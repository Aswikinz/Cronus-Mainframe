# CronusMainframe/utils/user_data.py

import csv
import os

class UserData:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.user_scores = {}
        self.user_voice_join_times = {}
        self.force_disconnect_threshold = 10  # Minimum time in seconds to be considered a forced disconnect

    def load_user_scores(self, guild_id):
        file_path = f"{self.data_directory}/{guild_id}_user_scores.csv"
        if not os.path.exists(file_path):
            self.user_scores[guild_id] = {}
        else:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                self.user_scores[guild_id] = {row['user_id']: {key: int(value) for key, value in row.items() if key != 'user_id'} for row in reader}

    def save_user_scores(self, guild_id):
        file_path = f"{self.data_directory}/{guild_id}_user_scores.csv"
        with open(file_path, 'w', newline='') as file:
            fieldnames = ['user_id', 'messages_sent', 'photos_sent', 'timeouts', 'force_disconnects', 'forced_deletions']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user_id, scores in self.user_scores[guild_id].items():
                scores['user_id'] = user_id
                writer.writerow(scores)

    def update_user_score(self, guild_id, user_id, key, value=1):
        if guild_id not in self.user_scores:
            self.load_user_scores(guild_id)

        if user_id not in self.user_scores[guild_id]:
            self.user_scores[guild_id][user_id] = {
                'messages_sent': 0,
                'photos_sent': 0,
                'timeouts': 0,
                'force_disconnects': 0,
                'forced_deletions': 0
            }

        self.user_scores[guild_id][user_id][key] += value
        self.save_user_scores(guild_id)

    def get_user_scores(self, guild_id):
        if guild_id not in self.user_scores:
            self.load_user_scores(guild_id)
        return self.user_scores[guild_id]

    def on_message(self, guild_id, user_id, has_attachment):
        self.update_user_score(guild_id, user_id, 'messages_sent')
        if has_attachment:
            self.update_user_score(guild_id, user_id, 'photos_sent')

    def on_message_delete(self, guild_id, user_id):
        self.update_user_score(guild_id, user_id, 'forced_deletions')

    def on_member_update(self, guild_id, user_id, timed_out):
        if timed_out:
            self.update_user_score(guild_id, user_id, 'timeouts')

    def on_voice_state_update(self, guild_id, user_id, joined_voice, left_voice):
        if joined_voice:
            self.user_voice_join_times[user_id] = time.time()
        elif left_voice and user_id in self.user_voice_join_times:
            join_time = self.user_voice_join_times.pop(user_id)
            duration = time.time() - join_time
            if duration >= self.force_disconnect_threshold:
                self.update_user_score(guild_id, user_id, 'force_disconnects')
