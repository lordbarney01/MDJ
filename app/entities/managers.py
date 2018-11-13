from app.entities.models import User, Playlist, Song
from abc import ABCMeta, abstractmethod
import json
from mongoengine.errors import DoesNotExist, ValidationError


class DocumentManager(metaclass=ABCMeta):
    entity_class = None
    all_keys = None

    @staticmethod
    def __generate_entity_json(keys, entity):
        entity_json = {}
        for key in keys:
            if key == 'id':  # Special case due to Document's default objectID
                entity_json[key] = str(getattr(entity, key))
            else:
                try:
                    attr = getattr(entity, key)
                    json.dumps(attr)
                    entity_json[key] = attr
                except TypeError:
                    continue
        return entity_json

    @classmethod
    def __get_entity_as_json(cls, keys, object_id):
        try:
            entity = cls.entity_class.objects(id=object_id).only(*keys).get()
            return cls.__generate_entity_json(keys=keys, entity=entity)
        except (DoesNotExist, ValidationError):
            return False

    @classmethod
    def __get_entity_list_as_json(cls, keys, **object_filter):
        entities = cls.entity_class.objects(**object_filter).only(*keys)

        if not len(entities):
            return []

        entity_list = []
        for entity in entities:
            entity_json = cls.__generate_entity_json(keys=keys, entity=entity)
            entity_list.append(entity_json)
        return entity_list

    @classmethod
    def __get_entity_list_as_json(cls, keys, **object_filter):
        entities = cls.entity_class.objects(**object_filter).only(*keys)

        if not len(entities):
            return []

        entity_list = []
        for entity in entities:
            entity_json = cls.__generate_entity_json(keys=keys, entity=entity)
            entity_list.append(entity_json)
        return entity_list

    @classmethod
    def get_full_entity_list_as_json(cls, **object_filter):
        """
        :param object_filter: A filter dictionary by which the list will be retrieved. I.E: {"acl": user_id}
        :return: A fully detailed list of the objects
        """
        return cls.__get_entity_list_as_json(cls.all_keys, **object_filter)

    @classmethod
    def get_entity_specific_keys(cls, entity_id, keys=None, **object_filter):
        """
        This method will return a mongoengine object (FOR INTERNAL USE ONLY)
        :param entity_id: object id (bson string)
        :param keys: keys array to retrieve
        :return: Entity mongoengine object
        """
        object_filter["id"] = entity_id
        result = cls.entity_class.objects(**object_filter).only(*keys)

        if len(result) == 1:
            return result[0]
        else:
            return RuntimeError("Error, duplicate entities for same id")

    @classmethod
    def get_entity_object_by_specific_keys(cls, **object_filter):
        result = cls.entity_class.objects(**object_filter)
        if len(result) == 1:
            return result[0]
        else:
            return RuntimeError("Error, duplicate entities for same id")

    @classmethod
    def does_entity_with_keys_exist(cls, **object_filter):
        result = cls.entity_class.objects(**object_filter)
        if len(result) > 0:
            return True
        else:
            return False

    @classmethod
    def get_entity_object(cls, entity_id=None, entity_name=None):
        """
        :param entity_id: Mongo object ID - optional
        :param entity_name: Mongo object name - optional
        :return: true/false on whether the object exists
        """
        if entity_id:
            try:
                return cls.entity_class.objects.get(id=entity_id)
            except Exception:
                return False
        elif entity_name:
            try:
                return cls.entity_class.objects.get(name=entity_name)
            except Exception:
                return False

    @classmethod
    @abstractmethod
    def create_entity(cls, **kwargs):
        new_entity = cls.entity_class(**kwargs)
        new_entity.save()
        return str(new_entity.id)


class UserManager(DocumentManager):
    entity_class = User
    all_keys = ['userName', 'playlists']


class SongManager(DocumentManager):
    entity_class = Song
    all_keys = ['youtubeUrl', 'songName', 'author', 'genre']

    @staticmethod
    def delete_song(youtubeUrl):
        Song.objects(youtubeUrl=youtubeUrl).delete()


class PlaylistManager(DocumentManager):
    entity_class = Playlist
    all_keys = ['songs', 'title', 'isPrivate']