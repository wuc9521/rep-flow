def get_HELP_HINT():
    return f"""
        <ul class='hint-font' onclick='handleHintClick(event)'> 
            <li><span>show help:</span><u>/help</u> </li> 
            <li><span>test bug:</span> <u>/test $BUG</u></li> 
            <li><span>show current state:</span> <u>/state</u></li> 
        </ul> 
    """


def get_NUMBER_EMBD_HINT(id):
    return f"""
        <ul class="hint-font" onclick='handleHintClick(event)' style="list-style-type: none;">
            <li><span>Monitoring Screen...</span></li>
            <li><span>Test:</span><span class='u-like'> [{id}] </span><span>launching...</span></li> 
            <li><span>Test:</span><span class='u-like'> [{id}] </span><span>launched...</span></li> 
        </ul>
    """

def get_CURRENT_STATE(id):
    if id >= 0:
        return f"""
            <ul class="hint-font" onclick='handleHintClick(event)' style="list-style-type: none;">
                <li><span>Monitoring Screen...</span></li>
                <li><span>Test:</span><span class='u-like'> [{id}] </span><span>ongoing...</span></li> 
            </ul>
        """
    else:
        return f"""
            <ul class="hint-font" onclick='handleHintClick(event)' style="list-style-type: none;">
                <li><span>Monitoring Screen...</span></li>
                <li><span>No test launched</span></li> 
            </ul>
        """
HELP = get_HELP_HINT()
