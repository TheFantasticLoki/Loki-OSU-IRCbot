# Node.js stage
FROM node:18 AS pp-calculator
WORKDIR /app/pp-service
COPY src/services/pp/package*.json ./
RUN npm install
COPY src/services/pp .

# Python stage
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install tmux and Node.js
RUN apt-get update && apt-get install -y tmux nodejs

# Copy Python bot code
COPY . .

# Copy PP calculator from Node.js stage
COPY --from=pp-calculator /app/pp-service /app/pp-service

# Create startup script with proper logging
RUN echo '#!/bin/bash\n\
tmux new-session -d -s osu-bot "node /app/pp-service/index.js 2>&1 | sed \"s/^/[pp-service] /\""\n\
tmux split-window -v "python /app/main.py"\n\
tmux pipe-pane -t osu-bot:0.0 "sed \"s/^/[pp-service] /\" >> /proc/1/fd/1"\n\
tmux pipe-pane -t osu-bot:0.1 "sed \"s/^/[bot] /\" >> /proc/1/fd/1"\n\
exec tail -f /dev/stdout /dev/stderr' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]