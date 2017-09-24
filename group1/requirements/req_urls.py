from django.conf.urls import patterns, include, url

from requirements.views import projects
from requirements.views import stories
from requirements.views import iterations
from requirements.views import users

urlpatterns = patterns('',
                       url(r'^changepasswd', users.changepasswd),
                       url(r'^userprofile', users.userprofile),

                       url(r'^projects', projects.list_projects),
                       url(r'^projectdetail/(?P<projectID>\d+)',
                           projects.project),
                       url(
                           r'^addusertoproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)',
                           projects.add_user_to_project),
                       url(
                           r'^removeuserfromproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)',
                           projects.remove_user_from_project),
                       url(r'^usersinproject/(?P<projectID>\d+)',
                           projects.list_users_in_project),

                       url(r'^newproject', projects.new_project),
                       url(r'^editproject/(?P<projectID>\d+)',
                           projects.edit_project),
                       url(r'^deleteproject/(?P<projectID>\d+)',
                           projects.delete_project),

                       url(r'^newiteration/(?P<projectID>\d+)',
                           iterations.new_iteration),
                       url(r'^edititeration/(?P<projectID>\d+)/(?P<iterationID>\d+)',
                           iterations.edit_iteration),
                       url(r'^deleteiteration/(?P<projectID>\d+)/(?P<iterationID>\d+)',
                           iterations.delete_iteration),
                       url(r'^iterations/(?P<projectID>\d+)',
                           iterations.list_iterations_for_project),
                       url(r'^iterationswithselection/(?P<projectID>\d+)/(?P<iterationID>\d+)',
                           iterations.list_iterations_for_project_with_selection),
                       # url(r'^shownewiteration/(?P<projectID>\d+)',projects.show_new_iteration),


                       url(r'^newstory/(?P<projectID>\d+)', stories.new_story),
                       url(r'^editstory/(?P<projectID>\d+)/(?P<storyID>\d+)',
                           stories.edit_story),
                       url(r'^deletestory/(?P<projectID>\d+)/(?P<storyID>\d+)',
                           stories.delete_story),
                       url(r'^movestorytoicebox/(?P<projectID>\d+)/(?P<storyID>\d)',
                           stories.move_story_to_icebox),
                       url(r'^movestorytoiter/(?P<projectID>\d+)/(?P<storyID>\d+)/(?P<iterationID>\d+)',
                           stories.move_story_to_iteration),
                       url(r'^tasks/(?P<storyID>\d+)', stories.list_tasks),
                       url(r'^comments/(?P<storyID>\d+)',
                           stories.list_comments),

                       # url(r'^newtask/(?P<projectID>\d+)/(?P<iterationID>\d+)/(?P<storyID>\d+)', stories.new_task),
                       url(r'^addtaskintolist/(?P<storyID>\d+)',
                           stories.add_task_into_list),
                       # url(r'^edittask/(?P<projectID>\d+)/(?P<iterationID>\d+)/(?P<storyID>\d+)/(?P<taskID>\d+)', stories.edit_task),
                       url(r'^edittaskinlist/(?P<storyID>\d+)/(?P<taskID>\d+)',
                           stories.edit_task_in_list),
                       # url(r'^deletetask/(?P<projectID>\d+)/(?P<iterationID>\d+)/(?P<storyID>\d+)/(?P<taskID>\d+)', stories.delete_task),
                       url(r'^removetaskfromlist/(?P<storyID>\d+)/(?P<taskID>\d+)',
                           stories.remove_task_from_list),

                       # url(r'^newcomment/(?P<projectID>\d+)/(?P<iterationID>\d+)/(?P<storyID>\d+)', stories.new_comment),
                       url(r'^addcommentintolist/(?P<storyID>\d+)',
                           stories.add_comment_into_list),
                       # url(r'^editcomment/(?P<storyID>\d+)', stories.list_tasks),
                       url(r'^editcommentinlist/(?P<storyID>\d+)/(?P<commentID>\d+)',
                           stories.edit_comment_in_list),
                       # url(r'^deletecomment/(?P<storyID>\d+)', stories.list_tasks),
                       url(r'^removecommentfromlist/(?P<storyID>\d+)/(?P<commentID>\d+)',
                           stories.remove_comment_from_list),

                       url(r'^iterationdetail/(?P<projectID>\d+)/(?P<iterationID>\d+)',
                           iterations.iteration),

                       url(r'^userprojectaccess/(?P<projectID>\d+)/(?P<userID>\d+)',
                           projects.manage_user_association),
                       url(r'^changeuserrole/(?P<projectID>\d+)/(?P<userID>\d+)',
                           projects.change_user_role),
                       url(r'^getattachments/(?P<projectID>\d+)',
                           projects.get_attachments),
                       url(r'^uploadprojectattachment/(?P<projectID>\d+)',
                           projects.upload_attachment),
                       url(r'^downprojectattach/(?P<projectID>\d+)/?',
                           projects.download_file),

                       )
