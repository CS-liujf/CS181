import tarfile

with tarfile.open('submit.tar', 'w') as out:
    out.add('logicPlan.py')
