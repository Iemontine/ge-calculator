import json

print("====GE REQUIREMENT CALCULATOR by dws ===\n")

# read input file and turn it into a json with the following form
"""
{
  "CHE 2A": {
       "satisfies": [
            "QL",
            "SE",
            "SL"
       ],
       "units": 5
  },
  ...
}
"""
courses = {}
with open("in.txt", "r") as f:
    for line in f.readlines():
        if ")" in line and line != "":
            name = line[0:line.index("(")-1]
            satisfies = line[line.index(")")+2:-1].replace(" ", "")
            
            courses[name] = {"satisfies": {}, "units": 0}
            courses[name]["satisfies"] = satisfies.split(",")
            courses[name]["units"] = int(line[line.index("(")+1:line.index("(")+2])
            with open("out.json", "w") as f2:
                json.dump(courses, f2, indent=5)

# load the GE requirements for graduation
requirements = {}
with open("requirements.json", "r") as f:
    requirements = json.load(f)

# create an empty dict to hold all the units that got applied and the courses that were applied for that unit
currentFulfilled = {}
for requirement in requirements:
    currentFulfilled[requirement] = {"units": 0, "courses": []}

coursesRemove = courses.copy() # copy the dict because we're going to be removing courses that were applied because courses only apply once to a GE

# first round
for course in courses: # loop through all courses
    for requirement in courses[course]["satisfies"]: # loop through each of the requirements that each course satisfies
        # first apply courses to requirements but make sure to fulfill as many requirements as possible
        if requirement in currentFulfilled and course in coursesRemove and currentFulfilled[requirement]["units"] - requirements[requirement] <= 0:
            currentFulfilled[requirement]["units"] += courses[course]["units"]
            currentFulfilled[requirement]["courses"].append(str(course))
            coursesRemove.pop(course)

# second round
for course in courses: # loop through all courses
    for requirement in courses[course]["satisfies"]: # loop through each of the requirements that each course satisfies
        # now apply remaining courses to what ever requirement it fits into, because all requirements that could have been fulfilled have been fulfilled
        if requirement in currentFulfilled and course in coursesRemove:
            currentFulfilled[requirement]["units"] += courses[course]["units"]
            currentFulfilled[requirement]["courses"].append(str(course))
            coursesRemove.pop(course)

# what remains in courseRemove at this point are courses that were not applied

print(f"You have completed {sum(course['units'] for course in currentFulfilled.values())} units so far.")
print(f"You have {sum(course['units'] for course in coursesRemove.values())} units that have not been applied from the following classes: {[course for course in coursesRemove]}.\n")

for requirement in requirements:
    need = currentFulfilled[requirement]['units'] - requirements[requirement]
    
    if currentFulfilled[requirement]['units']: # if the number of fulfilled units in this category is non-zero
        print(f"You fulfilled {currentFulfilled[requirement]['units']}/{requirements[requirement]} unit(s) of {requirement} using {currentFulfilled[requirement]['courses']}")
    else:
        print(f"You fulfilled {currentFulfilled[requirement]['units']}/{requirements[requirement]} unit(s) of {requirement}")

    if need < 0:
        print("You need " + str(abs(need)) + " more units of " + requirement)