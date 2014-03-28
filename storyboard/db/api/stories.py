# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from storyboard.db.api import base as api_base
from storyboard.db import models


def story_get(story_id):
    return api_base.entity_get(models.Story, story_id)


def story_get_all(marker=None, limit=None, project_id=None):
    if project_id:
        return _story_get_all_in_project(marker=marker,
                                         limit=limit,
                                         project_id=project_id)
    else:
        return api_base.entity_get_all(models.Story, is_active=True,
                                       marker=marker, limit=limit)


def story_get_count(project_id=None):
    if project_id:
        return _story_get_count_in_project(project_id)
    else:
        return api_base.entity_get_count(models.Story, is_active=True)


def _story_get_all_in_project(project_id, marker=None, limit=None):
    session = api_base.get_session()

    sub_query = api_base.model_query(models.Task.story_id, session) \
        .filter_by(project_id=project_id, is_active=True) \
        .distinct(True) \
        .subquery()

    query = api_base.model_query(models.Story, session) \
        .filter_by(is_active=True) \
        .join(sub_query, models.Story.tasks)

    query = api_base.paginate_query(query=query,
                                    model=models.Story,
                                    limit=limit,
                                    sort_keys=['id'],
                                    marker=marker,
                                    sort_dir='asc')

    return query.all()


def _story_get_count_in_project(project_id):
    session = api_base.get_session()

    sub_query = api_base.model_query(models.Task.story_id, session) \
        .filter_by(project_id=project_id, is_active=True) \
        .distinct(True) \
        .subquery()

    query = api_base.model_query(models.Story, session) \
        .filter_by(is_active=True) \
        .join(sub_query, models.Story.tasks)

    return query.count()


def story_create(values):
    return api_base.entity_create(models.Story, values)


def story_update(story_id, values):
    return api_base.entity_update(models.Story, story_id, values)


def story_delete(story_id):
    story = story_get(story_id)

    if story:
        story.is_active = False
        api_base.entity_update(models.Story, story_id, story.as_dict())