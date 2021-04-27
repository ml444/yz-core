
import os
import shutil
import stat
from os import path

import yzcore
from . import CommandError
from yzrpc.commands import CommandBase


class TemplateCommand(CommandBase):

    requires_system_checks = False
    # The supported URL schemes
    url_schemes = ['http', 'https', 'ftp']
    # Rewrite the following suffixes when determining the target filename.
    rewrite_template_suffixes = (
        # Allow shipping invalid .py files without byte-compilation.
        ('.py-tpl', '.py'),
    )

    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the application or project.')
        parser.add_argument('directory', nargs='?', help='Optional destination directory')
        # parser.add_argument('--template', help='The path or URL to load the template from.')

    def handle(self, app_or_project, name, target=None, **options):
        """

        :param app_or_project: "app" or "project"
        :param name: 工程或者应用名称
        :param target:
        :param options:
        :return:
        """
        self.app_or_project = app_or_project
        # self.paths_to_remove = []
        # self.verbosity = options['verbosity']

        self.validate_name(name, app_or_project)

        # if some directory is given, make sure it's nicely expanded
        if target is None:
            top_dir = path.join(os.getcwd(), name)
            try:
                os.makedirs(top_dir)
            except FileExistsError:
                raise CommandError("'%s' already exists" % top_dir)
            except OSError as e:
                raise CommandError(e)
        else:
            top_dir = os.path.abspath(path.expanduser(target))
            if not os.path.exists(top_dir):
                raise CommandError("Destination directory '%s' does not "
                                   "exist, please create it first." % top_dir)
            if self.app_or_project == "app":
                top_dir = path.join(top_dir, name)
                try:
                    os.makedirs(top_dir)
                except FileExistsError:
                    raise CommandError("'%s' already exists" % top_dir)
                except OSError as e:
                    raise CommandError(e)

        base_name = '%s_name' % app_or_project
        base_subdir = '%s_template' % app_or_project

        template_dir = path.join(yzcore.__path__[0], 'templates', base_subdir)
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):

            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace(base_name, name)
            # relative_dir = path_rest.replace(base_subdir, name)
            if relative_dir:
                target_dir = path.join(top_dir, relative_dir)
                if not path.exists(target_dir):
                    os.mkdir(target_dir)

            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = path.join(root, filename)
                new_path = path.join(top_dir, relative_dir,
                                     filename.replace(base_name, name))
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[:-len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if path.exists(new_path):
                    raise CommandError("%s already exists, overlaying a "
                                       "project or app into an existing "
                                       "directory won't replace conflicting "
                                       "files" % new_path)

                shutil.copyfile(old_path, new_path)

                # if self.verbosity >= 2:
                self.stdout.write("Creating %s\n" % new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except OSError:
                    self.stderr.write(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path, self.style.NOTICE)

    def validate_name(self, name, app_or_project):
        a_or_an = 'an' if app_or_project == 'app' else 'a'
        if name is None:
            raise CommandError('you must provide {an} {app} name'.format(
                an=a_or_an,
                app=app_or_project,
            ))

    def make_writeable(self, filename):
        """
        Make sure that the file is writeable.
        Useful if our source is read-only.
        """
        if not os.access(filename, os.W_OK):
            st = os.stat(filename)
            new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
            os.chmod(filename, new_permissions)
