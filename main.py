from get_tg_messages import *

tg_channels = {"xushnudbek":"t.me/xushnudbek",
               "trolluz":"t.me/trolluz",
               "davletovuz":"t.me/davletovuz",
               "zafarbek":"t.me/Zafarbek_Solijonov",
               "alimoff":"t.me/nurbekalimov",
               "fayzbog":"t.me/fayzboguz",
               "daliyev":"t.me/muxbir1",
               "makarenko":"t.me/makarenko_channel",
               "bakiroo":"t.me/the_bakiroo",
               "bahodirahmedov":"t.me/bahodirahmedoff",
               "muhrim":"t.me/muhrim",
               "shahnoza":"t.me/shahnozxon",
               "asanov":"t.me/AsanovEldar",
               "kurbanoff":"t.me/kurbanoffnet",
               "ruziohunov":"t.me/ruziohunov",
               "allaev":"t.me/allaevuzb"}

json_data = {}
domlajon = {"domlajon":"t.me/domlajon"}
sariqdev = {"sariqdev":"t.me/sariqdev"}
for key, value in sariqdev.items():
    json_data[key] = get_tg_messages(key,value,year=2020)

print(json_data)


