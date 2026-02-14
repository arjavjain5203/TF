import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Family Tree Bot API is running"}

@pytest.mark.asyncio
async def test_webhook_hello(client: AsyncClient):
    # Simulate a "Hi" message from a new user
    data = {"From": "whatsapp:+1234567890", "Body": "Hi"}
    # Twilio sends form data
    response = await client.post("/webhook", data=data)
    assert response.status_code == 200
    assert "Family Tree Bot" in response.text

@pytest.mark.asyncio
async def test_create_tree_flow(client: AsyncClient):
    phone = "whatsapp:+1234567891"
    
    # 1. Start with "Hi" or "Menu"
    await client.post("/webhook", data={"From": phone, "Body": "Hi"})
    
    # 2. Select Option 2 "Add Member" (which should trigger tree creation if none)
    response = await client.post("/webhook", data={"From": phone, "Body": "2"})
    assert "Enter the name" in response.text
    
    # 3. Enter Name
    response = await client.post("/webhook", data={"From": phone, "Body": "John Doe"})
    assert "Enter Date of Birth" in response.text
    
    # 4. Enter DOB
    response = await client.post("/webhook", data={"From": phone, "Body": "01-01-1980"})
    assert "Enter Gender" in response.text
    
    # 5. Enter Gender
    response = await client.post("/webhook", data={"From": phone, "Body": "Male"})
    assert "Enter Phone Number" in response.text
    
    # 6. Skip Phone
    response = await client.post("/webhook", data={"From": phone, "Body": "skip"})
    # Since it's the first member, it should finalize as Root and NOT ask for relation
    assert "Added John Doe to the tree" in response.text

@pytest.mark.asyncio
async def test_add_relative_flow(client: AsyncClient):
    phone = "whatsapp:+1234567892"
    
    # 1. Create Root Member first
    await client.post("/webhook", data={"From": phone, "Body": "Hi"})
    await client.post("/webhook", data={"From": phone, "Body": "2"}) # Add Member
    await client.post("/webhook", data={"From": phone, "Body": "Root User"})
    await client.post("/webhook", data={"From": phone, "Body": "01-01-1950"})
    await client.post("/webhook", data={"From": phone, "Body": "Male"})
    await client.post("/webhook", data={"From": phone, "Body": "skip"})
    
    # 2. Add Second Member
    await client.post("/webhook", data={"From": phone, "Body": "2"}) # Add Member
    await client.post("/webhook", data={"From": phone, "Body": "Child User"})
    await client.post("/webhook", data={"From": phone, "Body": "01-01-1980"})
    await client.post("/webhook", data={"From": phone, "Body": "Female"})
    response = await client.post("/webhook", data={"From": phone, "Body": "skip"})
    
    # Should ask for Relation since tree has members
    assert "Who is this member related to?" in response.text
    
    # 3. Select Relative (ID 1 should be Root User)
    response = await client.post("/webhook", data={"From": phone, "Body": "1"})
    assert "Is the new member a (1) Parent, (2) Child, or (3) Spouse" in response.text
    
    # 4. Select Relation Type (2 = Child)
    response = await client.post("/webhook", data={"From": phone, "Body": "2"})
    assert "Added Child User to the tree" in response.text

@pytest.mark.asyncio
async def test_view_tree(client: AsyncClient):
    phone = "whatsapp:+1234567893"
    # Create tree and member
    await client.post("/webhook", data={"From": phone, "Body": "Hi"})
    await client.post("/webhook", data={"From": phone, "Body": "2"})
    await client.post("/webhook", data={"From": phone, "Body": "Viewer"})
    await client.post("/webhook", data={"From": phone, "Body": "01-01-1990"})
    await client.post("/webhook", data={"From": phone, "Body": "Other"})
    await client.post("/webhook", data={"From": phone, "Body": "skip"})
    
    # View Tree
    response = await client.post("/webhook", data={"From": phone, "Body": "1"})
    assert "Your Family Tree" in response.text
    assert "Viewer" in response.text
