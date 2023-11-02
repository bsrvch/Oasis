import os, xml.etree.ElementTree as ET, argparse

class XmlParser:
    def __init__(self) -> None:
        self.__path = "pom.xml"
        self.work_path = "src/main/java/" + self.get_group_id().replace('.', '/') + "/" + self.get_project_name().lower() + "/"
    def get_group_id(self):
        try:
            for child in ET.parse(self.__path).getroot():
                if 'groupId' in child.tag:
                    return child.text
        except IOError as e:
            print(e)

    def get_project_name(self):
        try:
            for child in ET.parse(self.__path).getroot():
                if 'name' in child.tag:
                    return child.text.lower()
        except IOError as e:
            print(e)

class Controller:
        def __init__(self, parser) -> None:
            self.__parser = parser
            self.__conroller_dir = self.__parser.work_path + "controllers/"

        def __content(self, name):
            return "package " + self.__parser.get_group_id() + "." + self.__parser.get_project_name() + ".controllers" + ";\n\nimport org.springframework.stereotype.Controller;\nimport org.springframework.web.bind.annotation.GetMapping;\n\n@Controller\npublic class " + name + " {\n    @GetMapping(\"/\")\n    public String index() {\n        return \"index\";\n    }\n}\n"
        
        def make(self, name):
            dir = self.__conroller_dir
            if(not os.path.exists(dir)):
                os.mkdir(dir)
            if "/" in name:
                splitted = name.split("/")
                name = splitted[len(splitted) - 1]
                for i in range(0, len(splitted) - 2):
                    dir = dir + splitted[i] + "/"
                    if(not os.path.exists(dir)):
                        os.mkdir(dir)
                        

            name = name.replace("Repository", "")
            name = name.replace("Service", "")
            if not "Controller" in name:
                name+="Controller"
            
            if(not os.path.exists(dir + name + ".java")):
                controller = open(dir + name + ".java", "w+")
                controller.write(self.__content(name))
                controller.close
                print(name + " создан успешно")
            else:
                print(name + " уже существует!")

class Model:
    def __init__(self, parser) -> None:
        self.__parser = parser
        self.__model_dir = self.__parser.work_path + "models/"
    
    def __content(self, name):
        return "package "+ self.__parser.get_group_id() + "." + self.__parser.get_project_name() +".models;\n\nimport jakarta.persistence.*;\nimport lombok.AllArgsConstructor;\nimport lombok.Data;\nimport lombok.NoArgsConstructor;\n\n@Entity\n@Data\n//@Table(name =  your table name)\n@AllArgsConstructor\n@NoArgsConstructor\npublic class " + name + " {\n    @Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    @Column(name = \"id\")\n    private long id;\n\n    // Your code here\n\n}\n"

    def make(self, name):
        dir = self.__model_dir
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if "/" in name:
            splitted = name.split("/")
            name = splitted[len(splitted) - 1]
            for i in range(0, len(splitted) - 2):
                dir = dir + splitted[i] + "/"
                if(not os.path.exists(dir)):
                    os.mkdir(dir)
        name = name.replace("Controller", "")
        name = name.replace("Service", "")
        name = name.replace("Repository", "")
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if(not os.path.exists(dir + name + ".java")):
            model = open(dir + name + ".java", "w+")
            model.write(self.__content(name))
            model.close
            print(name + " создан успешно")
        else:
            print(name + " уже существует!")

class Service:
    def __init__(self, parser) -> None:
        self.__parser = parser
        self.__service_dir = self.__parser.work_path + "services/"

    def __content(self, name):
        return "package "+ self.__parser.get_group_id() + "." + self.__parser.get_project_name() +".services;\n\nimport org.springframework.stereotype.Service;\n\n@Service\npublic class " + name + " {\n // Your code here \n}"

    def make(self, name):
        dir = self.__service_dir
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if "/" in name:
            splitted = name.split("/")
            name = splitted[len(splitted) - 1]
            for i in range(0, len(splitted) - 2):
                dir = dir + splitted[i] + "/"
                if(not os.path.exists(dir)):
                    os.mkdir(dir)
        name = name.replace("Controller", "")
        name = name.replace("Repository", "")
        if not "Service" in name:
            name+="Service"
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if(not os.path.exists(dir + name + ".java")):
            service = open(dir + name + ".java", "w+")
            service.write(self.__content(name))
            service.close
            print(name + " создан успешно")
        else:
            print(name + " уже существует!")

class Repo:
    def __init__(self, parser) -> None:
        self.__parser = parser
        self.__repo_dir = self.__parser.work_path + "repositories/"

    def __content(self, name, with_model):
        if not with_model:
            return "package "+ self.__parser.get_group_id() + "." + self.__parser.get_project_name() +".repositories;\n\nimport org.springframework.data.jpa.repository.JpaRepository;\n\npublic interface " + name + " extends JpaRepository<, Long> {\n\n}"
        else:
            return "package "+ self.__parser.get_group_id() + "." + self.__parser.get_project_name() +".repositories;\n\nimport "+ self.__parser.get_group_id() + "." + self.__parser.get_project_name() +".models." + name.replace("Repository", "") + ";\nimport org.springframework.data.jpa.repository.JpaRepository;\n\npublic interface " + name + " extends JpaRepository<"+ name.replace("Repository", "") +", Long> {\n\n}"

    def make(self, name, with_model):
        dir = self.__repo_dir
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if "/" in name:
            splitted = name.split("/")
            name = splitted[len(splitted) - 1]
            for i in range(0, len(splitted) - 2):
                dir = dir + splitted[i] + "/"
                if(not os.path.exists(dir)):
                    os.mkdir(dir)
        name = name.replace("Controller", "")
        name = name.replace("Service", "")
        if not "Repository" in name:
            name+="Repository"
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        if(not os.path.exists(dir + name + ".java")):
            repo = open(dir + name + ".java", "w+")
            repo.write(self.__content(name, with_model))
            repo.close
            print(name + " создан успешно")
        else:
            print(name + " уже существует!")

class Manager:
    def __init__(self) -> None:
        self.parser = XmlParser()
        self.controller = Controller(parser=self.parser)
        self.model = Model(parser=self.parser)
        self.service = Service(parser=self.parser)
        self.repo = Repo(parser=self.parser)

if __name__ == '__main__':
    manager = Manager()
    parser = argparse.ArgumentParser(
                    prog='python -m manager.py',
                    description='creating someshit',
                    epilog='idi naxui')
    parser.add_argument("-c", "--controller",  type=str, nargs="+")
    parser.add_argument("-m", "--model",  type=str, nargs="+")
    parser.add_argument("-s", "--service",  type=str, nargs="+")
    parser.add_argument("-r", "--repo",  type=str, nargs="+")

    args = parser.parse_args()

    if args.repo:
        with_model = False
        try:
            if "m" in args.repo[1]:
                manager.model.make(args.repo[0])
                with_model = True
            if "c" in args.repo[1]:
                manager.controller.make(args.repo[0])
            if "s" in args.repo[1]:
                manager.service.make(args.repo[0])        
        except IndexError:
            pass
        manager.repo.make(args.repo[0], with_model=with_model)

    if args.model:
        with_model = True
        manager.model.make(args.model[0])
        try:
            if "c" in args.model[1]:
                manager.controller.make(args.model[0])
            if "s" in args.model[1]:
                manager.service.make(args.model[0])        
            if "r" in args.model[1]:
                manager.repo.make(args.model[0], with_model=with_model)
        except IndexError:
            pass

    if args.controller:
        with_model = False
        manager.controller.make(args.controller[0])
        try:
            if "m" in args.controller[1]:
                with_model = True
                manager.model.make(args.controller[0])
            if "s" in args.controller[1]:
                manager.service.make(args.controller[0])        
            if "r" in args.controller[1]:
                manager.repo.make(args.controller[0], with_model=with_model)
        except IndexError:
            pass
    
    if args.service:
        with_model = False
        manager.service.make(args.service[0])
        try:
            if "m" in args.service[1]:
                with_model = True
                manager.model.make(args.service[0])
            if "c" in args.service[1]:
                manager.controller.make(args.service[0])        
            if "r" in args.service[1]:
                manager.repo.make(args.service[0], with_model=with_model)
        except IndexError:
            pass