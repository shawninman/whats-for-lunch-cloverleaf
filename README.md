# whats-for-lunch-cloverleaf
 An AWS lambda for pulling lunch menus out of myschoolmenus.com for the Cloverleaf School District. This is in no way affiliated with myschoolmenus.com and is just for fun so my kids can ask the HomePod what's coming up for lunch

## Deployment notes

_probably mostly just for me_

Lambda wants all dependencies to be deployed flat in the same directory as the entrypoint file. It should be zipped up together like such:

```
cd package
zip -r ../for-deploy.zip .

cd ..
zip for-deploy.zip lunchViewer.py
```
