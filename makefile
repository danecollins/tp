
test:
	source ~/env/dj/bin/activate
	python manage.py test
	scripts/post_deploy_test local

.PHONY: test production
