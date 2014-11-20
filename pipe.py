import sys

class Pipe(object):

    def __init__(self):
        self.platform_name = {"linux2": "linux", "darwin": "mac", "win32": "windows"}[sys.platform]

    def context_from_path(self, path=""):

        path = path.replace(self.projects_path(), "")

        splitPath = path.split("/")[1:]
        project = splitPath[0]

        # Shot or asset context specifed
        if len(splitPath) == 4:
            if splitPath[1] == shot_work_area:
                context = {"platform": platform,
                           "project": project,
                           "work_area": shot_work_area,
                           "seq": splitPath[2],
                           "shot": splitPath[3]}

            elif splitPath[1] == asset_work_area:
                context = {"platform": platform,
                           "project": project,
                           "work_area": asset_work_area,
                           "asset_type": splitPath[2],
                           "asset": splitPath[3]}

        # Just a project specified
        elif len(splitPath) == 1:
            context = {"platform": platform,
                       "project": project}
        else:
            print "Can't make context out of given path."
            exit()

        return context


    def current_context_paths(self):

        context = self.context_from_path()
        projects_path = self.projects_path()

        # Set current project path
        context = self.context_from_path()
        current_project_path = "%s/%s" % (projects_path,
                                          context["project"])

        # Set current context path
        if "work_area" in context:
            # Shot work area
            if context["work_area"] == shot_work_area:
                current_context_path = "%s/%s/%s/%s/%s" % (projects_path,
                                                           context["project"],
                                                           context["work_area"],
                                                           context["seq"],
                                                           context["shot"])

            # Asset work area
            elif context["work_area"] == asset_work_area:
                current_context_path = "%s/%s/%s/%s/%s" % (projects_path,
                                                           context["project"],
                                                           context["work_area"],
                                                           context["asset_type"],
                                                           context["asset"])

            return {"project": current_project_path,
                    "context": current_context_path}

        else:

            return {"project": current_project_path}


# pipe = Pipe()
# pprint(pipe.app_launch_dictionary)
# print pipe.current_context_paths()
#print pipe.list_projects()
# print pipe.list_contexts()

