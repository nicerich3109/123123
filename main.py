import discord
from discord import app_commands
from discord.ext import commands
import io

# Включаем необходимые интенты
intents = discord.Intents.default()
intents.members = True  # ВАЖНО: включите в Discord Developer Portal (Privileged Gateway Intents)
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Словарь ролей: {ID роли: Название}
ROLES = {
    1525147604227198976: "New",
    1525147528700494055: "Main",
    1544281442266259506: "Legit",
    1525147233228685353: "Recrut",
    1525147059672580187: "Chief Recrut",
    1525147163313573928: "High",
    1525248468405453031: "Dep.Own",
}

# Порядок вывода ролей (от младшей к старшей)
ROLE_ORDER = [
    1525147604227198976,  # New
    1525147528700494055,  # Main
    1544281442266259506,  # Legit
    1525147233228685353,  # Recrut
    1525147059672580187,  # Chief Recrut
    1525147163313573928,  # High
    1525248468405453031,  # Dep.Own
]


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано {len(synced)} слэш-команд")
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")
    print(f"Бот запущен как {bot.user}")


@bot.tree.command(name="list", description="Собрать список участников по ролям и выложить в txt-файле")
async def list_members(interaction: discord.Interaction):
    await interaction.response.defer()  # ответ может занять время

    guild = interaction.guild
    if guild is None:
        await interaction.followup.send("Команду можно использовать только на сервере.")
        return

    lines = []
    lines.append(f"Список участников сервера: {guild.name}")
    lines.append(f"Всего участников на сервере: {guild.member_count}")
    lines.append("=" * 50)
    lines.append("")

    total_found = 0

    for role_id in ROLE_ORDER:
        role = guild.get_role(role_id)
        role_name = ROLES.get(role_id, "Unknown")

        lines.append(f"=== {role_name} (ID: {role_id}) ===")

        if role is None:
            lines.append("  [Роль не найдена на сервере]")
            lines.append("")
            continue

        members_with_role = [m for m in guild.members if role in m.roles]

        # Сортируем по имени
        members_with_role.sort(key=lambda m: m.display_name.lower())

        if not members_with_role:
            lines.append("  [Нет участников с этой ролью]")
        else:
            for idx, member in enumerate(members_with_role, 1):
                lines.append(
                    f"  {idx}. {member.display_name} ({member.name}) — ID: {member.id}"
                )
            total_found += len(members_with_role)

        lines.append("")

    lines.append("=" * 50)
    lines.append(f"Итого учтено записей: {total_found}")

    content = "\n".join(lines)

    # Создаём файл в памяти
    file = discord.File(
        fp=io.BytesIO(content.encode("utf-8")),
        filename="members_list.txt"
    )

    await interaction.followup.send(
        content=f"✅ Список готов! Найдено записей: **{total_found}**",
        file=file
    )


# Вставьте свой токен
bot.run("ВАШ_ТОКЕН_ЗДЕСЬ")