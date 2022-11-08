def set_min_max_values(station,search_range_dict ,vpvs_min=1.68, vpvs_max=1.98, Moho_min=40, Moho_max=90):
    search_range_dict[station]={}
    search_range_dict[station]["vpvs_min"]=vpvs_min
    search_range_dict[station]["vpvs_max"]=vpvs_max
    search_range_dict[station]["Moho_min"]=Moho_min
    search_range_dict[station]["Moho_max"]=Moho_max
    return search_range_dict



################### tunable parameters #######

#vp in the crust
vp=6.2

#weights for stacking
w_ps=1
w_ppps=1
w_ppss=1

#station name
stations = ["C008",]

search_range_dict={}

# set search area to default value for all stations
for station in stations:
    search_range_dict=set_min_max_values(station,search_range_dict)

# update values for specific stations, for example:
search_range_dict=set_min_max_values("C008",search_range_dict,  Moho_min=35)  # set minimum Moho depth of search area to 35 km (instead of default 40 km )

##############################################


