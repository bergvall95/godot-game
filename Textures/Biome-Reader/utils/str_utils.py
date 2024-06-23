

alien_chars = ['/', '<', '>', ':', '"', '/', '\\', '|', '?', '*']


def is_illegal_string(string):
    """check if string has illegal char"""

    return any( (char in alien_chars) for char in string )


def legal(string):
    """make string legal"""

    if is_illegal_string(string):
        return ''.join(char for char in string if (not char in alien_chars) )
    
    return string 


def find_suffix(basename, collection_api, zeros=3,): 
    """find suffix with name that do not exists yet"""

    i = 1
    new = basename 
    while (new in collection_api):
        suffix_idx = f"{i:03d}" if (zeros==3) else f"{i:02d}"
        new = f"{basename}.{suffix_idx}"
        i += 1

    return new 


def no_names_in_double(string, list_strings, startswith00=False, n=3,):
    """return a correct string with suffix to avoid doubles"""
    #used heavily in masks creation, to get correct names 
    #I Guess that this fct is a clone of find_suffix() ? 

    if (startswith00):
        #Always have suffix, startswith .00

        x=string
        i=0
        if (string+".00" not in list_strings):
            return string + ".00"

        while (f"{x}.{i:02d}" in list_strings):
            i += 1

        return f"{x}.{i:02d}" 

    #else Normal Behavior
    x=string 
    i=1
    while (x in list_strings):
        x = string + f".{i:03d}" if n==3 else string + f".{i:02d}"
        i +=1

    if (string!=x):
        return x

    return string 


def word_wrap(string="", layout=None, alignment="CENTER", max_char=70, active=False, alert=False, icon=None, scale_y=1.0,):
    """word wrap a piece of string""" 
    
    import bpy

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences 
    max_char = int(max_char*addon_prefs.ui_word_wrap_max_char_factor)
    scale_y = addon_prefs.ui_word_wrap_y*scale_y
    
    
    def wrap(string,max_char):
        """word wrap function""" 

        original_string = string
        newstring = ""
        
        while (len(string) > max_char):

            # find position of nearest whitespace char to the left of "width"
            marker = max_char - 1
            while (marker >= 0 and not string[marker].isspace()):
                marker = marker - 1

            # If no space was found, just split at max_char
            if (marker==-1):
                marker = max_char
    
            # remove line from original string and add it to the new string
            newline = string[0:marker] + "\n"
            newstring = newstring + newline
            string = string[marker + 1:]

        return newstring + string


    #Multiline string? 
    if ("\n" in string):
          wrapped = "\n".join([wrap(l,max_char) for l in string.split("\n")])
    else: wrapped = wrap(string,max_char)

    #UI Layout Draw? 

    if (layout is not None):

        from .. resources.icons import cust_icon

        lbl = layout.column()
        lbl.active = active 
        lbl.alert = alert
        lbl.scale_y = scale_y

        for i,l in enumerate(wrapped.split("\n")):

            if alignment:

                line = lbl.row()
                line.alignment = alignment

                if (icon and (i==0)):

                    if (icon.startswith("W")):
                        line.label(text=l, icon_value=cust_icon(icon),)    
                        continue      

                    line.label(text=l, icon=icon)    
                    continue

                line.label(text=l)
                continue 

            lbl.label(text=l)
            continue
        
    return wrapped


def smart_round(f):
    """return float value with rounding appropriate depending on decimal value"""
    if (f<0.0001):
        return round(f,6)
    if (f<0.001):
        return round(f,5)
    if (f<0.01):
        return round(f,4)
    if (f<0.1):
        return round(f,3)
    if (f<1.0):
        return round(f,2)
    if (f<100):
        return round(f,1)
    return int(f)


def square_area_repr(f):
    """stringify squarearea to cm²/m²/ha/km²"""
    
    if (f<0.1):
        return f"{int(f*10_000)} cm²"
    
    if (f<5_000):
        return f"{f:.1f} m²"
    
    if (f<1_000_000):
        return f"{f/10_000:.1f} ha"
    
    else: #above 100ha == km²
        return f"{f/1_000_000:.1f} km²"


def count_repr(f, unit="",):
    """get string version of scatter count"""

    return "..." if (f==-1) else f'{f:,} {unit}'


def version_to_float(s, truncated=False):
    """versioning is very dumb in this plugin, it sometimes use string format, sometimes blender use a list format ect.. ultimately in order to """
        
    if isinstance(s, (list, tuple, set)):
        s = '.'.join(map(str, s))
        
    # remove unwanted substrings
    for sub in ["Beta", "Alpha", "Release", "Candidate", " "]:
        s = s.replace(sub, "")
    
    # split on dot and rejoin the first two parts with a dot, concatenate the rest
    parts = s.split('.')
    s = '.'.join(parts[:2]) + ''.join(parts[2:])
    
    # convert to float
    s = float(s)
    
    # truncate to only essential version?
    if (truncated):
        s = int(s*10)/10

    return s