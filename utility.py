import re

def stn_firm_name(target, unabbreviate=False, nolegal=False, parentheses=False):
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
    
    if type(target) == str:
        # Convert to uppercase
        target = target.upper()
        
        # Remove characters in parentheses
        if parentheses == True:
            target = re.sub("[\(\[].*?[\)\]]", "", target)
        
        # Keep A/C, C/O, D/B/A, and F/K/A together before replace
        target = re.sub(" A\/C( |$)", " AC ", target)
        target = re.sub(" C\/O( |$)", " CO ", target)
        target = re.sub(" D\/B\/A/?( |$)", " DBA ", target)
        target = re.sub(" D\/B\/$", " DBA", target)
        target = re.sub(" F\/K\/A/?( |$)", " FKA ", target)
        
        # Remove text after DBA/FKA
        target = re.sub(" (DBA|FKA)( |$).*", "", target)
        
        # Remove "the"
        target = re.sub("^THE ", "", target)
        target = re.sub(" THE\s*$", "", target)
        
        
        # Clean organizational forms
        target = re.sub(" COMPANY( |$)", " CO ", target)
        target = re.sub(" CORPORATION( |$)", " CORP ", target)
        target = re.sub(" FEDERAL CREDIT UNION$", " FCU", target)
        target = re.sub(" CREDIT UNION$", " CU", target)
        target = re.sub(" ( A)? FEDERAL SAVINGS BANK *$", " FSB", target)
        target = re.sub(" F S B *$", " FSB", target)
        target = re.sub(" INCORPORATED( |$)", " INC ", target)
        target = re.sub(" LIMITED LIABILITY CO *$", " LLC", target)
        target = re.sub(" (LIMITED|LTD) PARTNERSHIP *$", " LP", target)
        target = re.sub(" LIMITED *$", " LTD", target)
        target = re.sub(" P L L C *$", " PLLC", target)
        target = re.sub(" L L C *$", " LLC", target)
        target = re.sub(" L L L P *$", " LLLP", target)
        target = re.sub(" L L P *$", " LLP", target)
        target = re.sub(" L P *$", " LP", target)
        target = re.sub(" M D( |$)", " MD ", target)
        target = re.sub(" NATIONAL ASSOCIATION *$", " NA", target)
        target = re.sub(" N A *$", " NA", target)
        target = re.sub(" P A *$", " PA", target)
        target = re.sub(" PROFESSIONAL ASSOCIATION *$", " PA", target)
        target = re.sub(" P L C *$", " PLC", target)
        target = re.sub("( A)? STATE SAVINGS BANK *$", " SSB", target)
        target = re.sub(" S S B *$", " SSB", target)
        target = re.sub("(^| )U S A( |$)", " USA ", target)
        
        # Remove symbols
        for symbol in symbols:
            target = target.replace(symbol, "")
        
        if unabbreviate == True:
            target = re.sub(" ASSN( |$)", " ASSOCIATION ", target)
            target = re.sub(" BCH( |$)", " BEACH ", target)
            target = re.sub(" INTL( |$)", " INTERNATIONAL ", target)
            target = re.sub(" (MGMT|MGT)( |$)", " MANAGEMENT ", target)
            target = re.sub(" MKT( |$)", " MARKET ", target)
            target = re.sub(" SR?VCS( |$)", " SERVICES ", target)
        
        if nolegal == True:
            target = re.sub(" (CORP|CO|INC|LLC|LLLP|LLP|LTD)\s*$", "", target)
