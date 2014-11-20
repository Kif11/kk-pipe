import os


class Util(object):

    def __init__(self):
        self.project_list = self.list_projects()

    def list_projects(self):

        projects_directory = self.projects_directory()
        projects = os.listdir(projects_directory)

        return projects

    def walklevel(self, some_dir, level):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def list_contexts(self, userProject):

        # if not self.context_from_path()["project"] in self.list_projects():
        # print "Can't find the specified project"
        # else:
        # project_path = self.current_context_paths()["project"]
        project_path = self.projects_directory() + "/" + userProject

        for root, dirs, files in self.walklevel(project_path, 3):
            print root.replace("\\", "/")


    def context_from_path(self, projects_directory=None, full_context_path=None):

        # Stripe project directory from path
        full_context_path = full_context_path.replace(projects_directory, "")
        splitPath = full_context_path.split("/")[1:]
        project = splitPath[0]

        shot_work_area = "shot"
        asset_work_area = "asset"

        # Shot or asset context specifed
        if len(splitPath) == 2:
            if splitPath[1] == shot_work_area:
                context = {"project": project,
                           "work_area": shot_work_area}

            elif splitPath[1] == asset_work_area:
                context = {"project": project,
                           "work_area": asset_work_area,
                           "asset_type": splitPath[2],
                           "asset": splitPath[3]}

        # Just a project specified
        elif len(splitPath) == 1:
            context = {"project": project}
        else:
            raise Exception("Can't make context out of given path")

        return context

# util = Util()
#print util.context_from_path("F:/p")
# print util.list_contexts("Curpigeon")