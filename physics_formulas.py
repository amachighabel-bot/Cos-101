a="a for velocity"
b="b for acceleration"
c="c for force"
d="d for work_done"
e="e for potential_energy"
formulas=[a, b, c, d, e]
print(formulas)
home=input("Select a formula: ")
if home=="a":
   distance=float(input("Enter distance: "))
   time=float(input("Enter time: "))
   print("The velocity is", distance/time)
elif home=="b":
    velocity=float(input("Enter the velocity: "))
    time_1=float(input("Enter the time: "))
    print("The acceleration is", velocity/time_1)
elif home=="c":
    mass=float(input("Enter the mass of the object: "))
    acceleration=float(input("Input acceleration: "))
    print("The force is", mass*acceleration)
elif home=="d":
    force=float(input("Input force: "))
    distance=float(input("Input distance: "))
    print("The work done is", force*distance)
elif home=="e":
    mass=float(input("Input mass: "))
    acceleration=float(input("Input acceleration due to gravity: "))
    height=float(input("Input height: "))
    print("The potential energy is", mass*height*acceleration)
else:
    print("Unavailable...")