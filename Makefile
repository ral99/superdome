unit_test_modules = $(shell find unit_tests -name "*_test.py")

# $(call test_judge,cmd,ret)
define test_judge
ifeq ($2,0)
	expression = "\033[32m$1\033[m"
else
	expression = "\033[31m$1\033[m"
endif
endef

# $(call run_test,cmd)
define run_test
$(eval RET := $(shell python $1 2> /dev/null; echo $$?))
$(eval $(call test_judge,$1,$(RET)))
@echo $(expression)
endef

.PHONY: all unit_test

all: unit_test

unit_test:
	$(info ================================== Unit tests ==================================)
	$(foreach one, $(unit_test_modules), $(call run_test,$(one)))
	@echo ""
