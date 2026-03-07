from hidden_gems import check_nearby_gems

user_lat = 27.1752
user_lon = 78.0420
user_id = "demo_user"

unlocked = check_nearby_gems(user_lat, user_lon, user_id)

print(unlocked)