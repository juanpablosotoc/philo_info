from fastapi import APIRouter
from .schema import CreateExampleInput, CreateEngineInput
from .. import user_db_dependancy
from bson import ObjectId


data_route = APIRouter(prefix='/data', tags=['data'])

@data_route.get('/')
async def index_get(user_db: user_db_dependancy, example_id: str):
    result = user_db.db.get_document('trainingData', {'_id': ObjectId(example_id)})
    # close the session
    user_db.db.disconnect()
    return {**result, 'engine_id': str(result['engine_id'])}


@data_route.post('/')
async def index_post(user_db: user_db_dependancy, example_input: CreateExampleInput):
    data = {
        'engine_id': ObjectId(example_input.engine_id),
        'tag': example_input.tag,
    }
    if example_input.children is not None:
        data['children'] = example_input.children
    
    result = user_db.db.insert_document('trainingData', data)
    # close the session
    user_db.db.disconnect()
    return result


@data_route.put('/')
async def index_put(user_db: user_db_dependancy, example_id: str, example_input: CreateExampleInput):
    data = {
        'engine_id': ObjectId(example_input.engine_id),
        'tag': example_input.tag,
    }
    if example_input.children is not None:
        data['children'] = example_input.children
    result = user_db.db.replace_document('trainingData', {'_id': ObjectId(example_id)}, data)
    # close the session
    user_db.db.disconnect()
    return result


@data_route.delete('/')
async def index_delete(user_db: user_db_dependancy, example_id: str):
    result = user_db.db.delete_document('trainingData', {'_id': ObjectId(example_id)})
    # close the session
    user_db.db.disconnect()
    return result


@data_route.get('/engines')
async def engines_get(user_db: user_db_dependancy):
    result = user_db.db.get_documents('engines', {})
    # close the session
    user_db.db.disconnect()
    return result


@data_route.post('/engines')
async def engines_post(user_db: user_db_dependancy, create_engine_input: CreateEngineInput):
    result = user_db.db.insert_document('engines', {'engine_name': create_engine_input.engine_name, 'creation_date': create_engine_input.creation_date})
    # close the session
    user_db.db.disconnect()
    return result


@data_route.get('/engines/{engine_id}')
async def engines_get_by_id(engine_id: str, user_db: user_db_dependancy):
    result = user_db.db.get_document('engines', {'_id': ObjectId(engine_id)})
    # close the session
    user_db.db.disconnect()
    return result


@data_route.get('/engines/{engine_id}/trainingData')
async def engines_training_data_get(engine_id: str, user_db: user_db_dependancy):
    result = user_db.db.get_documents('trainingData', {'engine_id': ObjectId(engine_id)})
    # close the session
    user_db.db.disconnect()
    return [ {**doc, 'engine_id': str(doc['engine_id'])} for doc in result ]
