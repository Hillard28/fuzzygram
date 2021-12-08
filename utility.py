import re

def stn_firm(target, unabbreviate=False, nolegal=False, parentheses=False):
    symbols = [
        ",",
        ".",
        ":",
        ";",
        "(",
        ")",
        "*",
        "\\",
        "-",
        "?",
        "\'",
        "\"",
        "[",
        "]",
        "{",
        "}",
        "!",
        "_",
        "/",
        "`",
        "<",
        ">"
    ]
    
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Remove characters in parentheses
        if parentheses == True:
            retarget = re.sub("[\(\[].*?[\)\]]", "", retarget)
        
        # Keep A/C, C/O, D/B/A, and F/K/A together before replace
        retarget = re.sub(" A\/C( |$)", " AC ", retarget)
        retarget = re.sub(" C\/O( |$)", " CO ", retarget)
        retarget = re.sub(" D\/B\/A/?( |$)", " DBA ", retarget)
        retarget = re.sub(" D\/B\/$", " DBA", retarget)
        retarget = re.sub(" F\/K\/A/?( |$)", " FKA ", retarget)
        
        # Remove symbols
        for symbol in symbols:
            retarget = retarget.replace(symbol, "")
        
        # Replace +
        retarget = re.sub("^A \+ ", "A+ ", retarget)
        if re.match("^A\+ ", retarget) is None:
            retarget = retarget.replace("+", " & ")
        
        # Remove spaces between single letter words
        search = re.search("^([A-Z] ([A-Z] )+[A-Z]) ", retarget)
        if search is not None:
            name = search[0].replace(" ", "")
            retarget = name + re.sub("^[A-Z] ([A-Z] )+[A-Z] ", " ", retarget)
        else:
            search = re.search("^([A-Z] [A-Z]) ", retarget)
            if search is not None:
                name = search[0].replace(" ", "")
                retarget = name + re.sub("^[A-Z] [A-Z] ", " ", retarget)
            else:
                search = re.search("^([A-Z] & [A-Z]) ", retarget)
                if search is not None:
                    name = search[0].replace(" ", "")
                    retarget = name + re.sub("^[A-Z] & [A-Z] ", " ", retarget)
        
        # Remove text after DBA/FKA
        retarget = re.sub(" (DBA|FKA)( |$).*", "", retarget)
        
        # Remove "the"
        retarget = re.sub("^THE ", "", retarget)
        retarget = re.sub(" THE\s*$", "", retarget)
        
        # Clean organizational forms
        retarget = re.sub(" COMPANY( |$)", " CO ", retarget)
        retarget = re.sub(" CORPORATION( |$)", " CORP ", retarget)
        retarget = re.sub(" FEDERAL CREDIT UNION$", " FCU", retarget)
        retarget = re.sub(" CREDIT UNION$", " CU", retarget)
        retarget = re.sub(" ( A)? FEDERAL SAVINGS BANK *$", " FSB", retarget)
        retarget = re.sub(" F S B *$", " FSB", retarget)
        retarget = re.sub(" INCORPORATED( |$)", " INC ", retarget)
        retarget = re.sub(" LIMITED LIABILITY CO *$", " LLC", retarget)
        retarget = re.sub(" (LIMITED|LTD) PARTNERSHIP *$", " LP", retarget)
        retarget = re.sub(" LIMITED *$", " LTD", retarget)
        retarget = re.sub(" P L L C *$", " PLLC", retarget)
        retarget = re.sub(" L L C *$", " LLC", retarget)
        retarget = re.sub(" L L L P *$", " LLLP", retarget)
        retarget = re.sub(" L L P *$", " LLP", retarget)
        retarget = re.sub(" L P *$", " LP", retarget)
        retarget = re.sub(" M D( |$)", " MD ", retarget)
        retarget = re.sub(" NATIONAL ASSOCIATION *$", " NA", retarget)
        retarget = re.sub(" N A *$", " NA", retarget)
        retarget = re.sub(" P A *$", " PA", retarget)
        retarget = re.sub(" PROFESSIONAL ASSOCIATION *$", " PA", retarget)
        retarget = re.sub(" P L C *$", " PLC", retarget)
        retarget = re.sub("( A)? STATE SAVINGS BANK *$", " SSB", retarget)
        retarget = re.sub(" S S B *$", " SSB", retarget)
        retarget = re.sub("(^| )U S A( |$)", " USA ", retarget)
        
        # Replace AND
        retarget = re.sub(" AND ", " & ", retarget)
        retarget = re.sub(" &AMP ", " & ", retarget)
        retarget = re.sub("&APOS ", "", retarget)
        
        # Remove #
        retarget = retarget.replace("#", "")
        
        # Replace @
        retarget = retarget.replace("@", "AT")
        
        # Unabbreviate
        if unabbreviate == True:
            retarget = re.sub(" ASSN( |$)", " ASSOCIATION ", retarget)
            retarget = re.sub(" BCH( |$)", " BEACH ", retarget)
            retarget = re.sub(" INTL( |$)", " INTERNATIONAL ", retarget)
            retarget = re.sub(" (MGMT|MGT)( |$)", " MANAGEMENT ", retarget)
            retarget = re.sub(" MKT( |$)", " MARKET ", retarget)
            retarget = re.sub(" SR?VCS( |$)", " SERVICES ", retarget)
        
        # Remove legal classifications
        if nolegal == True:
            retarget = re.sub(" (CORP|CO|INC|LLC|LLLP|LLP|LTD)\s*$", "", retarget)
        
        # Strip white space
        retarget = retarget.strip()
        retarget = " ".join(retarget.split())
        
        return retarget
    
    else:
        return target

def stn_street(target):
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Remove suite numbers
        retarget = re.sub(" (APT|FLOOR|STE|SUITE|UNIT).*", "", retarget)
        
        # Remove punctuation
        retarget = retarget.replace("#", "")
        retarget = retarget.replace(".", "")
        
        # Replace street designations
        retarget = re.sub(" AVENUE( |$)", " AVE ", retarget)
        retarget = re.sub(" BOULEVARD( |$)", " BLVD ", retarget)
        retarget = re.sub(" COURT( |$)", " CT ", retarget)
        retarget = re.sub(" DRIVE( |$)", " DR ", retarget)
        retarget = re.sub(" HIGHWAY( |$)", " HWY ", retarget)
        retarget = re.sub(" LANE( |$)", " LN ", retarget)
        retarget = re.sub(" PARKWAY( |$)", " PKWY ", retarget)
        retarget = re.sub(" PLACE( |$)", " PL ", retarget)
        retarget = re.sub(" PLAZA( |$)", " PLZ ", retarget)
        retarget = re.sub(" STATE ROAD( |$)", " SR ", retarget)
        retarget = re.sub(" STATE RD( |$)", " SR ", retarget)
        retarget = re.sub(" ROAD( |$)", " RD ", retarget)
        retarget = re.sub(" STREET( |$)", " ST ", retarget)
        retarget = re.sub(" TERRACE( |$)", " TER ", retarget)
        retarget = re.sub(" TRAIL( |$)", " TRL ", retarget)
        
        # Remove 1st, 2nd, 3rd, etc
        search = re.match("^(.*)([0-9])(ND|RD|ST|TH)( |$)(.*)$", retarget)
        if search is not None:
            retarget = search[1] + search[2] + " " + search[5]
        
        retarget = retarget.replace("FIRST", "1")
        retarget = retarget.replace("SECOND", "2")
        retarget = retarget.replace("THIRD", "3")
        retarget = retarget.replace("FOURTH", "4")
        retarget = retarget.replace("FIFTH", "5")
        retarget = retarget.replace("SIXTH", "6")
        retarget = retarget.replace("SEVENTH", "7")
        retarget = retarget.replace("EIGTH", "8")
        retarget = retarget.replace("NINTH", "9")
        retarget = retarget.replace("TENTH", "10")
        
        # Remove numbers after street name
        if re.match(" (AVE|BLVD|CT|DR|HWY|LN|PKWY|PL|PLZ|RD|SR|ST|TER|TRL|WAY) [-0-9]+\s*$", retarget) is not None:
            retarget = re.sub(" [0-9]+\s*$", "", retarget)
        
        # Abbreviate cardinal directions
        re.sub(" NORTH( |$)", " E ", retarget)
        re.sub(" EAST( |$)", " E ", retarget)
        re.sub(" SOUTH( |$)", " E ", retarget)
        re.sub(" WEST( |$)", " E ", retarget)
        
        re.sub(" NORTHEAST( |$)", " E ", retarget)
        re.sub(" NORTH EAST( |$)", " E ", retarget)
        re.sub(" SOUTHEAST( |$)", " E ", retarget)
        re.sub(" SOUTH EAST( |$)", " E ", retarget)
        
        re.sub(" NORTHWEST( |$)", " E ", retarget)
        re.sub(" NORTH WEST( |$)", " E ", retarget)
        re.sub(" SOUTHWEST( |$)", " E ", retarget)
        re.sub(" SOUTH WEST( |$)", " E ", retarget)
        
        # Strip white space
        retarget = retarget.strip()
        retarget = " ".join(retarget.split())
        
        return retarget
    
    else:
        return target
