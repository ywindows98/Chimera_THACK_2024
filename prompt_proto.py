
attr_names = ["ID", "Name", "Number"]
d_types = ["int64", "string", "float64"]

attr_type = []
attributes = ""
for i in range(len(attr_names)):
    attr_type.append(f"{attr_names[i]} of type {d_types[i]}")
    attributes+=f" {attr_type[i]}, "



print(f"""You have information about potential dataset: attributes names, their data types, and possibly their descriptions. Using this information, only you need to write code that strictly solves the task I will describe.
Preferably using pandas and pyplot. Do not create any mockup of the potential dataset. Always save resulting plot figures using plt.savefig(plot_name, transparent=True). Make and save separate figures for each small request.
Attributes are: {attributes}.""")