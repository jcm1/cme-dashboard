#!/usr/bin/env python3
"""CME KPI Dashboard updater.
Rebuilds index.html from template.html + data/cme_kpi_data.json, and appends new datapoints.

Commands:
  rebuild                          regenerate index.html from current data
  add-month  --period 2026-07 --adv-total 30.1 [--adv rates=15.0,equity=8.1,...] [--oi rates=xx,...]
  add-quarter --period 2026Q3 --rev 1680 [--adj-opex 525] [--blend 0.67] [--rpc rates=0.46,...]
             [--buybacks 400] [--savings 97] [--perf-bonds 168] [--price 2026-09-30=255]
             [--fees 1390 --md 240] [--adj-eps 3.05] [--oi rates=84.3,equity=10.2,...]  (P8-P12 series)
             [--opex comp=233,tech=83,prof=29,amort=56,depr=28,other=60]  (P13; needs --opex-g,
              licensing & other fees stored as exact residual = opex_g - the six lines)
  set --path capital.reg_div_ps.2027 --value 5.6     surgical edit
Every mutation appends to data/audit_log.jsonl with timestamp + args. Run rebuild after edits.
GitHub Pages flow: commit data/ + index.html; the URL is always current."""
import json, sys, argparse, datetime, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT/"data"/"cme_kpi_data.json"
TPL  = ROOT/"template.html"
OUT  = ROOT/"index.html"
LOG  = ROOT/"data"/"audit_log.jsonl"

def load(): return json.load(open(DATA))
def save(d):
    json.dump(d, open(DATA,"w"), indent=1)
def audit(action, args):
    with open(LOG,"a") as f:
        f.write(json.dumps({"ts":datetime.datetime.utcnow().isoformat(),"action":action,"args":args})+"\n")

def rebuild():
    d = load()
    tpl = open(TPL).read()
    blob = "const DATA = " + json.dumps(d) + ";"
    out = re.sub(r"/\*DATA_START\*/.*?/\*DATA_END\*/",
                 "/*DATA_START*/\n"+blob+"\n/*DATA_END*/", tpl, flags=re.S)
    open(OUT,"w").write(out)
    print(f"rebuilt index.html ({len(out)//1024}KB) through {d['meta']['through']}")

def kv(s):
    return {k: float(v) for k,v in (pair.split("=") for pair in s.split(","))}

def add_month(a):
    d = load()
    if a.adv_total is not None:
        d["adv_total"] = [x for x in d["adv_total"] if x["p"]!=a.period]
        d["adv_total"].append({"p":a.period,"adv":a.adv_total,"src":"monthly volume release R"})
    if a.oi:
        d["moat"]["oi_by_class"]["series"].append({"p":a.period,**kv(a.oi),"src":"monthly release R"})
    d["meta"]["through"]["monthly"] = a.period
    save(d); audit("add-month", vars(a)); rebuild()

def add_quarter(a):
    d = load()
    if a.rev is not None:
        d["quarterly_fin"] = [x for x in d["quarterly_fin"] if x["p"]!=a.period]
        row = {"p":a.period,"rev":a.rev,"opex_g":a.opex_g,"opinc_g":(a.rev-a.opex_g) if a.opex_g else None,"src":"release R"}
        if a.adj_opex: row["adj_opex"]=a.adj_opex; row["adj_opinc"]=a.rev-a.adj_opex
        d["quarterly_fin"].append(row)
    if a.blend or a.rpc or a.adv:
        entry = d["byline"].setdefault(a.period, {"src":"release R/D"})
        if a.blend: entry["blend"]=a.blend
        if a.rpc: entry.setdefault("rpc",{}).update(kv(a.rpc))
        if a.adv: entry.setdefault("adv",{}).update(kv(a.adv))
    if a.buybacks is not None:
        d["capital"]["buybacks_m"] = [x for x in d["capital"]["buybacks_m"] if x["p"]!=a.period]
        d["capital"]["buybacks_m"].append({"p":a.period,"v":a.buybacks,"src":"release R"})
    if a.savings: d["moat"]["margin_savings_bpd"].append({"p":a.period,"v":a.savings,"src":"R"})
    if a.perf_bonds: d["moat"]["perf_bonds_b"].append({"p":a.period,"v":a.perf_bonds,"src":"R"})
    if a.price:
        dt,px = a.price.split("="); d["price"].append({"d":dt,"px":float(px),"src":"R/aggregator"})
    if a.fees is not None and a.md is not None and a.rev is not None:
        d["rev_breakdown"] = [x for x in d.get("rev_breakdown",[]) if x["p"]!=a.period]
        d["rev_breakdown"].append({"p":a.period,"fees":a.fees,"md":a.md,"other":round(a.rev-a.fees-a.md,1),"total":a.rev,"src":"release R"})
    if a.adj_eps is not None:
        d["adj_eps"] = [x for x in d.get("adj_eps",[]) if x["p"]!=a.period]
        d["adj_eps"].append({"p":a.period,"v":a.adj_eps,"src":"release R"})
    if a.oi:
        s = d["moat"]["oi_by_class"]["series"]
        d["moat"]["oi_by_class"]["series"] = [x for x in s if x["p"]!=a.period]+[{"p":a.period,**kv(a.oi),"src":"release R"}]
    if a.opex:
        v = kv(a.opex); need = ["comp","tech","prof","amort","depr","other"]
        missing = [k for k in need if k not in v]
        if missing or a.opex_g is None:
            sys.exit(f"--opex needs {','.join(need)} plus --opex-g (missing: {missing or '--opex-g'})")
        lic = round(a.opex_g - sum(v[k] for k in need), 1)
        s = d.setdefault("opex_breakdown", {"series": []})["series"]
        d["opex_breakdown"]["series"] = [x for x in s if x["p"]!=a.period]+[
            {"p":a.period, **{k:v[k] for k in ["comp","tech","prof","amort","depr"]},
             "lic":lic, "other":v["other"], "total":a.opex_g}]
    if a.adv_q: 
        d["adv_total"] = [x for x in d["adv_total"] if x["p"]!=a.period]
        d["adv_total"].append({"p":a.period,"adv":a.adv_q,"src":"R"})
    d["meta"]["through"]["quarterly"] = a.period
    save(d); audit("add-quarter", vars(a)); rebuild()

def set_path(a):
    d = load(); node = d; keys = a.path.split(".")
    for k in keys[:-1]: node = node[k]
    try: val = json.loads(a.value)
    except: val = a.value
    node[keys[-1]] = val
    save(d); audit("set", vars(a)); rebuild()

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("rebuild")
m = sub.add_parser("add-month"); m.add_argument("--period",required=True); m.add_argument("--adv-total",type=float,dest="adv_total"); m.add_argument("--oi")
q = sub.add_parser("add-quarter"); q.add_argument("--period",required=True)
for arg,typ in [("--rev",float),("--opex-g",float),("--adj-opex",float),("--blend",float),("--buybacks",float),("--savings",float),("--perf-bonds",float),("--adv-q",float),("--fees",float),("--md",float),("--adj-eps",float)]:
    q.add_argument(arg,type=typ,dest=arg[2:].replace("-","_"),default=None)
q.add_argument("--rpc"); q.add_argument("--adv"); q.add_argument("--price"); q.add_argument("--oi"); q.add_argument("--opex")
s = sub.add_parser("set"); s.add_argument("--path",required=True); s.add_argument("--value",required=True)
a = p.parse_args()
{"rebuild":lambda x:rebuild(),"add-month":add_month,"add-quarter":add_quarter,"set":set_path}[a.cmd](a)
