with open("pasenger-service/pom.xml", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "t\t</dependency>" in line or "<dependency>" in line and "t\t<groupId>" in line:
        continue  # skip broken lines
    new_lines.append(line)

content = "".join(new_lines)
# I'll just rewrite the whole file safely from a template or just inject the dependency properly
