from tailwind_palette import TailwindPalette as tp

class Colors:
    shades = [100,200,300,400,500,600,700,800,900,950]

    gray   = {str(s): tp.get(f"gray-{s}").hex    for s in shades}
    slate  = {str(s): tp.get(f"slate-{s}").hex   for s in shades}
    zinc   = {str(s): tp.get(f"zinc-{s}").hex    for s in shades}
    neutral= {str(s): tp.get(f"neutral-{s}").hex for s in shades}

    red    = {str(s): tp.get(f"red-{s}").hex     for s in shades}
    orange = {str(s): tp.get(f"orange-{s}").hex  for s in shades}
    amber  = {str(s): tp.get(f"amber-{s}").hex   for s in shades}
    yellow = {str(s): tp.get(f"yellow-{s}").hex  for s in shades}
    lime   = {str(s): tp.get(f"lime-{s}").hex    for s in shades}
    green  = {str(s): tp.get(f"green-{s}").hex   for s in shades}
    emerald= {str(s): tp.get(f"emerald-{s}").hex for s in shades}
    teal   = {str(s): tp.get(f"teal-{s}").hex    for s in shades}
    cyan   = {str(s): tp.get(f"cyan-{s}").hex    for s in shades}
    sky    = {str(s): tp.get(f"sky-{s}").hex     for s in shades}
    blue   = {str(s): tp.get(f"blue-{s}").hex    for s in shades}
    indigo = {str(s): tp.get(f"indigo-{s}").hex  for s in shades}
    violet = {str(s): tp.get(f"violet-{s}").hex  for s in shades}
    purple = {str(s): tp.get(f"purple-{s}").hex  for s in shades}
    fuchsia= {str(s): tp.get(f"fuchsia-{s}").hex for s in shades}
    pink   = {str(s): tp.get(f"pink-{s}").hex    for s in shades}
    rose   = {str(s): tp.get(f"rose-{s}").hex    for s in shades}