PORT=8080
CI_REGISTRY_IMAGE=jmalloc/echo-server:exp-feat-1ecfd275763eff1d6b4844ea3168962458c9f27a
PROXY_STATUS=ext
.PHONY: generate-yaml update-proxy deploy-container deploy-proxy delete-prev-container deploy cleanup

generate-yaml:
	python3 gen.py $(PREV_SHA) $(CURR_SHA) $(BRANCH_NAME) $(PORT) $(PROXY_STATUS)
update-proxy: generate-yaml
	docker exec envoy mv /var/lib/envoy/cds-new.yaml /var/lib/envoy/cds.yaml && mv /var/lib/envoy/lds-new.yaml /var/lib/envoy/lds.yaml
deploy-proxy:
	docker run --name envoy -d -p 80:10000 -p 9901:9901 -v ${PWD}/envoy.yaml:/etc/envoy/envoy.yaml -v ${PWD}/yaml:/var/lib/envoy --network envoy envoyproxy/envoy-alpine:v1.16.0
deploy-container:
	docker run --name $(BRANCH_NAME)-$(CURR_SHA) --hostname $(BRANCH_NAME)-$(CURR_SHA) -d --network envoy $(CI_REGISTRY_IMAGE)
delete-prev-container:
	docker container rm -f $(BRANCH_NAME)-$(PREV_SHA) 2> /dev/null || true

init: generate-yaml deploy-container deploy-proxy delete-prev-container

deploy: | generate-yaml deploy-container update-proxy delete-prev-container

cleanup: generate-yaml update-proxy delete-prev-container