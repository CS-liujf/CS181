import tarfile

with open('autograder.py') as f:
    exec(f.read())

with tarfile.open('submit.tar', 'w') as out:
    out.add('logicPlan.py')
