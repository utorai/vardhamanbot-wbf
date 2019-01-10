FROM utorai/botbase

# Set work directory as xbot which is the work directory for bot base.
WORKDIR /xbot

#Install Dependencies
RUN pipenv install --skip-lock azure-cosmosdb-table

# Copy training utterances and rasa config
COPY ./bot/data/rasa.md /xbot/vardhamanbot/bot/data/rasa.md
COPY ./bot/config/rasa.yml /xbot/vardhamanbot/bot/config/rasa.yml

# Train Rasa NLU for the desired intents.
RUN pipenv run python -m rasa_nlu.train -c ./vardhamanbot/bot/config/rasa.yml --data ./vardhamanbot/bot/data/rasa.md -o models --fixed_model_name nlu --project vardhamanbot --verbose 

# Copy the bot directory to the work directory.
COPY . /xbot/vardhamanbot

EXPOSE 8080

CMD pipenv run python ./vardhamanbot/bot/main.py