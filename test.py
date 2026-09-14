from schemas.user import User, UserCreate, UserUpdate

user = User(
    id = 1,
    name = "John",
    city="Abuja"
)

new_user= UserCreate(
    name = "Peter",
    city = "Lagos"
)

updated_user = UserUpdate(
    name = "Peter Uploaded",
    city = "Lekki"
)

print (user)
print(new_user)
print(updated_user)