# Deploy Preview
This project was inspired by deployment preview netifly. Trying to brings deployment preview not only for frontend apps, but also for backend apps. It will deploy your app to staging server using envoy-proxy (for routing) and docker container.

![Deployment Preview Gitlab + Envoy](https://user-images.githubusercontent.com/22183588/103174975-1b4a9180-4899-11eb-9d17-cfe58cd81888.png)


TODO:
- [ ] Support for Gitlab CI
- [ ] Support for Github Actions

#### Init Envoy Proxy
```
make init PREV_SHA=0000000000000000000000000000000000000000 CURR_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat PROXY_STATUS=new
```
### Deploy new container from feature branch
New MR
```
make deploy PREV_SHA=0000000000000000000000000000000000000000 CURR_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat
```
Upate Commit in MR
```
make deploy PREV_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a CURR_SHA=2ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat
```

### Cleanup container & proxy after MR
```
make cleanup PREV_SHA=2ecfd275763eff1d6b4844ea3168962458c9f27a CURR_SHA=2ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat
``` 

#### Generate Yaml

New branch
```
make generate-yaml PREV_SHA=0000000000000000000000000000000000000000 CURR_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat PORT=5000
```
Existing branch
```
make generate-yaml PREV_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a CURR_SHA=2daafd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat PORT=5000
```

#### Deploy Container

```
make deploy-container PREV_SHA=0000000000000000000000000000000000000000 CURR_SHA=1ecfd275763eff1d6b4844ea3168962458c9f27a BRANCH_NAME=exp-feat
```