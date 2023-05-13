bundle:
	#$(MAKE) -C src
	cp src/simplecalc service/ro/
	rm -f ../simplecalc.tgz
	tar caf ../simplecalc.tgz *
	@echo "#### Double check ../sample_c.tgz and submit it :) ####"

clean:
	#rm -fr service/ro
	#rm -rf service/rw

scriptbot_scripts:
	docker build -t $(SERVICE_NAME)_scripts ./scripts
