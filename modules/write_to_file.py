from lib_vendor import yaml

data = {"path":"C:/test22", "path2":"D:/blaaAAAA"}
with open('config/hou_session.yml', 'w') as yaml_file:
    yaml_file.write( yaml.dump(data, default_flow_style=False))