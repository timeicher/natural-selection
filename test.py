
class food:
    food_pos_x = [1,2,3]

food_size = 10
current_scan_x = 2


class sucker:

    ab = [2]
    def kill_me(ab):
        for food in ab:
            if food <= current_scan_x <= food+food_size:
                print("NICE")


sucker.kill_me(sucker.ab)