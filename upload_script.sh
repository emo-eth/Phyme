#!/bin/sh

version=$(echo "from Phyme import version; print(version)" | python)

git add .
git commit -m "version update"
git push origin master
git tag $version
git push --tags origin master
python setup.py sdist
twine upload dist/*