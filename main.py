import json
import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as file:
        players_data = json.load(file)
    for nickname, player_data in players_data.items():
        race_data = player_data.get("race", {})
        guild_data = player_data.get("guild")
        email = player_data.get("email")
        bio = player_data.get("bio")

        race, created = Race.objects.get_or_create(
            name=race_data.get("name"),
            defaults={"description": race_data.get("description", "")}
        )

        skills = race_data.get("skills", [])
        for skill_data in skills:
            Skill.objects.get_or_create(
                name=skill_data.get("name"),
                defaults={"bonus": skill_data.get("bonus", ""), "race": race}
            )

        guild = None
        if guild_data is not None:
            guild, created = Guild.objects.get_or_create(
                name=guild_data.get("name"),
                defaults={"description": guild_data.get("description")}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": email,
                "bio": bio,
                "race": race,
                "guild": guild
            }
        )


if __name__ == "__main__":
    main()
