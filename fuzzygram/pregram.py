"""
Tool for processing strings prior to fuzzy matching with fuzzygram
"""
import re
import unicodedata

def stn_firm(target, unabbreviate=False, noordinal=True, nolegal=False, parentheses=False):
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
        
        # Remove ordinals
        if noordinal == True:
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
        
        # Strip white space
        retarget = retarget.strip()
        retarget = " ".join(retarget.split())
        
        # Remove legal classifications
        if nolegal == True:
            retarget = re.sub(" (CORP|CO|INC|LLC|LLLP|LLP|LP|LTD)\s*$", "", retarget)
        
        return retarget
    
    else:
        return target

def stn_street(target):
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Remove suite numbers
        retarget = re.sub(" (APT|FLOOR|FL|STE|SUITE|UNIT).*", "", retarget)
        
        # Remove punctuation
        retarget = retarget.replace("#", "")
        retarget = retarget.replace(".", "")
        retarget = retarget.replace(",", "")
        
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
        
        # Remove PO Box
        retarget = retarget.replace("P O BOX", "")
        retarget = retarget.replace("PO BOX", "")
        
        # Strip white space
        retarget = retarget.strip()
        retarget = " ".join(retarget.split())
        
        # Remove numbers after street name
        if re.search(" (AVE|BLVD|CT|DR|HWY|LN|PKWY|PL|PLZ|RD|SR|ST|TER|TRL|WAY) [0-9]+\s*$", retarget) is not None:
            retarget = re.sub(" [0-9]+\s*$", "", retarget)
        
        # Abbreviate cardinal directions
        retarget = re.sub(" NORTH( |$)", " N ", retarget)
        retarget = re.sub(" EAST( |$)", " E ", retarget)
        retarget = re.sub(" SOUTH( |$)", " S ", retarget)
        retarget = re.sub(" WEST( |$)", " W ", retarget)
        
        retarget = re.sub(" NORTHEAST( |$)", " NE ", retarget)
        retarget = re.sub(" NORTH EAST( |$)", " NE ", retarget)
        retarget = re.sub(" SOUTHEAST( |$)", " SE ", retarget)
        retarget = re.sub(" SOUTH EAST( |$)", " SE ", retarget)
        
        retarget = re.sub(" NORTHWEST( |$)", " NW ", retarget)
        retarget = re.sub(" NORTH WEST( |$)", " NW ", retarget)
        retarget = re.sub(" SOUTHWEST( |$)", " SW ", retarget)
        retarget = re.sub(" SOUTH WEST( |$)", " SW ", retarget)
        
        # Remove only numbers
        if retarget.isdigit() == True:
            retarget = ""
        
        return retarget
    
    else:
        return target

def stn_city(target):
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Replace common descriptors
        retarget = re.sub(" BCH( |$)", " BEACH ", retarget)
        retarget = re.sub("^FT\.? ", "FORT ", retarget)
        retarget = re.sub("^PT\.? ", "PORT ", retarget)
        retarget = re.sub(" SPGS( |$)", " SPRINGS ", retarget)
        retarget = re.sub("^SAINT ", "ST ", retarget)
        
        # Abbreviate cardinal directions
        retarget = re.sub(" NORTH( |$)", " N ", retarget)
        retarget = re.sub(" EAST( |$)", " E ", retarget)
        retarget = re.sub(" SOUTH( |$)", " S ", retarget)
        retarget = re.sub(" WEST( |$)", " W ", retarget)
        
        retarget = re.sub(" NORTHEAST( |$)", " NE ", retarget)
        retarget = re.sub(" NORTH EAST( |$)", " NE ", retarget)
        retarget = re.sub(" SOUTHEAST( |$)", " SE ", retarget)
        retarget = re.sub(" SOUTH EAST( |$)", " SE ", retarget)
        
        retarget = re.sub(" NORTHWEST( |$)", " NW ", retarget)
        retarget = re.sub(" NORTH WEST( |$)", " NW ", retarget)
        retarget = re.sub(" SOUTHWEST( |$)", " SW ", retarget)
        retarget = re.sub(" SOUTH WEST( |$)", " SW ", retarget)
        
        # Strip white space
        retarget = retarget.strip()
        retarget = " ".join(retarget.split())
        
        return retarget
    
    else:
        return target

def stn_phone(target):
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
        
        # Remove symbols
        for symbol in symbols:
            retarget = retarget.replace(symbol, "")
        
        # Strip white space
        retarget = retarget.strip()
        retarget = "".join(retarget.split())
        
        return retarget
    
    else:
        return target

def stn_full_name(target, drop=False, fl=True, comma=False, whitespace=True):
    first = ""
    middle = ""
    last = ""
    suffix = ""
    credentials = ""
    
    symbols = [
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
    
    credentials_list = [
        "CPA",
        "DR",
        "ESQ",
        "MBA",
        "MD",
        "PHD"
    ]
    
    suffix_list = [
        "SR",
        "JR",
        "IV",
        "III",
        "II"
    ]
    
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Remove symbols
        for symbol in symbols:
            retarget = retarget.replace(symbol, "").strip()
            retarget = " ".join(retarget.split())
        
        # Remove MRS|MR|Owner at end
        if re.search("[A-Z]?(MRS|MR|OWNER)$", retarget) is not None:
            retarget = re.sub("(MRS|MR|OWNER)$", "", retarget)
            retarget = " ".join(retarget.split())
        
        # Extract credentials
        for credential in credentials_list:
            if re.search(" [A-Z]?" + credential + "$", retarget) is not None:
                credentials = credentials + " " + credential
                retarget = re.sub(credential + "$", "", retarget)
            elif re.search(" " + credential + " ", retarget) is not None:
                credentials = credentials + " " + credential
                retarget = re.sub(" " + credential + " ", " ", retarget)
        if re.search(" [A-Z]?JD$", retarget) is not None:
            credentials = credentials + " " + "JD"
            retarget = re.sub("JD$", "", retarget)
        
        # Extract suffixes
        for suff in suffix_list:
            if re.search(" [A-Z]?" + suff + "$", retarget) is not None and re.search(" ZIV$", retarget) is None:
                suffix = suffix + " " + suff
                suffix = suffix.strip()
                retarget = re.sub(suff + "$", "", retarget).strip()
            elif re.search(" " + suff + "[, ]", retarget) is not None and re.search(" ZIV$", retarget) is None:
                suffix = suffix + " " + suff
                retarget = re.sub(" " + suff + "[, ]", ", ", retarget)
                retarget = " ".join(retarget.split())
        
        if comma == False:
            retarget = retarget.replace(",", "")
        
        # Extract names
        if comma and fl == False:
            search = re.search("^([^,]+)", retarget)
            if search is not None:
                last = search[0]
                retarget = re.sub("^([^,]+)", ", ", retarget)
            
            search = re.search("^([^,]+)", retarget)
            if search is not None:
                first = search[0]
                retarget = re.sub("^([^,]+)(, |$)", "", retarget)
            
            search = re.search("[^, ]+)$", retarget)
            if search is not None:
                middle = search[0]
        
        elif comma == False and fl == False:
            search = re.search("^((DE LA|DE LOS|DE|DI|ST|VAN DER|VAN|VON)? ?[-'A-Z]+)", retarget)
            if search is not None:
                last = search[0]
                retarget = retarget.replace(last, "", 1).strip()
            
            search = re.search("^([-'A-Z]+)", retarget)
            if search is not None:
                first = search[0]
            
            middle = retarget.replace(first, "", 1).strip()
        
        elif fl:
            search = re.search("^([-'A-Z]+)", retarget)
            if search is not None:
                first = search[0]
                retarget = re.sub("^[-'A-Z]+ ", " ", retarget)
            
            search = re.search(" ((DE LA|DE LOS|DE|DI|ST|VAN DER|VAN|VON)? ?[-'A-Z]+)$", retarget)
            if search is not None:
                last = search[0]
                retarget = retarget.replace(last, "", 1).strip()
            
            middle = retarget
        
        # Strip white space
        first = first.strip()
        first = " ".join(first.split())
        middle = middle.strip()
        middle = " ".join(middle.split())
        if whitespace:
            last = " ".join(last.split())
        else:
            last = "".join(last.split())
        suffix = suffix.strip()
        suffix = " ".join(suffix.split())
        credentials = credentials.strip()
        
        if drop:
            return first + " " + middle + " " + last + " " + suffix
        else:
            return [first, middle, last, suffix, credentials]

def stn_name(target, comma=False, whitespace=True):
    symbols = [
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
    
    credentials_list = [
        "CPA",
        "DR",
        "ESQ",
        "MBA",
        "MD",
        "PHD"
    ]
    
    suffix_list = [
        "SR",
        "JR",
        "IV",
        "III",
        "II"
    ]
    
    if type(target) is str:
        # Convert to uppercase
        retarget = target.upper()
        
        # Remove symbols
        for symbol in symbols:
            retarget = retarget.replace(symbol, "").strip()
            retarget = " ".join(retarget.split())
        
        # Remove MRS|MR|Owner at end
        if re.search("[A-Z]?(MRS|MR|OWNER)$", retarget) is not None:
            retarget = re.sub("(MRS|MR|OWNER)$", "", retarget)
            retarget = " ".join(retarget.split())
        
        # Extract credentials
        for credential in credentials_list:
            if re.search(" [A-Z]?" + credential + "$", retarget) is not None:
                retarget = re.sub(credential + "$", "", retarget)
            elif re.search(" " + credential + " ", retarget) is not None:
                retarget = re.sub(" " + credential + " ", " ", retarget)
        if re.search(" [A-Z]?JD$", retarget) is not None:
            retarget = re.sub("JD$", "", retarget)
        
        # Extract suffixes
        for suff in suffix_list:
            if re.search(" [A-Z]?" + suff + "$", retarget) is not None and re.search(" ZIV$", retarget) is None:
                retarget = re.sub(suff + "$", "", retarget).strip()
            elif re.search(" " + suff + "[, ]", retarget) is not None and re.search(" ZIV$", retarget) is None:
                retarget = re.sub(" " + suff + "[, ]", ", ", retarget)
                retarget = " ".join(retarget.split())
        
        if comma == False:
            retarget = retarget.replace(",", "")
        
        # Strip white space
        retarget = retarget.strip()
        if whitespace:
            retarget = " ".join(retarget.split())
        else:
            retarget = "".join(retarget.split())
        
        return retarget

def soundex(target):

    if not target:
        return ""

    target = unicodedata.normalize("NFKD", target)
    target = target.upper()

    replacements = (
        ("BFPV", "1"),
        ("CGJKQSXZ", "2"),
        ("DT", "3"),
        ("L", "4"),
        ("MN", "5"),
        ("R", "6"),
    )
    result = [target[0]]
    count = 1

    # find would-be replacment for first character
    for lset, sub in replacements:
        if target[0] in lset:
            last = sub
            break
    else:
        last = None

    for letter in target[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            if letter != "H" and letter != "W":
                # leave last alone if middle letter is H or W
                last = None
        if count == 4:
            break

    result += "0" * (4 - count)
    return "".join(result)
