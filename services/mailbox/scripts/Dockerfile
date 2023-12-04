# The service author can use whatever start image he wants and whatever language/dependencies
# he wants

# ---- START AREA THAT CAN BE MODIFIED
FROM python:3.8.16-alpine3.18

#RUN apt-get update && apt-get install -y python3 python3-pip 

RUN pip3 install pycryptodome requests
RUN pip3 install attrs --force
# ---- END AREA THAT CAN BE MODIFIED

# The final 4 scripts/binaries (setflag, getflag, benign and exploit) need to be
# put in the folder /ictf and that folder need to be in the PATH
#
# THIS PART IS MANDATORY AND IT SHOULD NOT BE CHANGED!
WORKDIR /ictf/

COPY . .

RUN chmod +x ./benign ./getflag ./setflag

ENV PATH="/ictf/:${PATH}"

CMD /bin/bash
