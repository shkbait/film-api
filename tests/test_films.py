import pytest
from httpx import AsyncClient,ASGITransport
from src.main import app
from src.model.film import Film_Model

# @pytest.mark.asyncio
# async def test_sync_endpoint():
#     async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
#         response= await ac.get("/films")
#         print(response)
#         data=response.json()
#         assert response.status_code==200
#         assert len(data)==2

# @pytest.mark.asyncio
# async def test_post_endpoint():
#     async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
#         response= await ac.post("/films",json={"title":"Test","director":"Test"})
#         print(response)
#         data=response.json()
#         assert response.status_code==200
#         assert data=={"message": "Film added successfully"}

@pytest.mark.asyncio
async def test_id_find():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
        response=await ac.post(
            "/films",
            params={
                "title": "Test",
                "director": "Test",
                "genre": "Test",
                "year": "2009",
                "rating": "10",
            }
        )
        print(response)
        data=response.json()
        film_id=data["film_id"]
        get= await ac.get(f"/films/{film_id}")
        assert response.status_code==200
        assert data["film_id"]==film_id

@pytest.mark.asyncio
async def test_add():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
        # response= await ac.post("/films",json={"title":"Test","director":"Test"})
        response=await ac.post(
            "/films",
            params={
                "title": "Test",
                "director": "Test",
                "genre": "Test",
                "year": "2009",
                "rating": "10",
            }
        )
        print(response)
        data=response.json()
        assert response.status_code==200

@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
        # response= await ac.post("/films",json={"title":"Test","director":"Test"})
        response=await ac.post(
            "/films",
            params={
                "title": "Test delete",
                "director": "Test",
                "genre": "Test",
                "year": "2009",
                "rating": "10",
            }
        )
        print(response)
        data=response.json()
        film_id=data["film_id"]
        delete=await ac.delete(f"/films/{film_id}")
        assert delete.status_code==200
        check = await ac.get(f"/films/{film_id}")
        assert check.status_code == 404

@pytest.mark.asyncio
async def test_patch():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver")as ac:
        response=await ac.post(
                        "/films",
            params={
                "title": "Test delete",
                "director": "Test",
                "genre": "Test",
                "year": "2009",
                "rating": "1",
            }
        )
        print(response)
        data=response.json()
        film_id=data["film_id"]
        patch_test=await ac.patch(
            f"/films/{film_id}",
            params={
                "title": "Test delete",
                "director": "Test",
                "genre": "Test",
                "year": "2009",
                "rating": "10",
            }
            )
        data_2=patch_test.json()
        rate=data_2["rating"]
        assert patch_test.status_code==200
        assert data_2["rating"]==10

        


