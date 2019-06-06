
test:
	source ~/env/tp3/bin/activate
	python manage.py test
	scripts/post_deploy_test local

.PHONY: test production
