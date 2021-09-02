def get_role_string(role_name):
    if(role_name.startswith('t')):
        return 'top'
    if(role_name.startswith('j')):
        return 'jungle'
    if(role_name.startswith('m')):
        return 'middle'
    if(role_name.startswith('a')):
        return 'adc'
    if(role_name.startswith('b')):
        return 'adc'
    if(role_name.startswith('s')):
        return 'support'


def get_champion_alias(champion):
    championstring = champion.lower()
    if(championstring == "j4" or championstring == "jarvan iv"):
        return "jarvaniv"
    if(championstring == "kha'zix" or championstring == "kha" or championstring == "kha6"):
        return "khazix"
    if(championstring == "kai'sa"):
        return "kaisa"
    if(championstring == "rek'sai"):
        return "reksai"
    if(championstring == "nunu & willump" or championstring == "nunu&willump" or championstring == "nunu willump"):
        return "nunu"
    return championstring
