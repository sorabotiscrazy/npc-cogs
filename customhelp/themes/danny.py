from ..core.base_help import (
    BaguetteHelp,
    pagify,
    EmbedField,
    EMPTY_STRING,
    Context,
    CategoryConvert,
    HelpSettings,
    _,
    discord,
    commands,
    box,
    GLOBAL_CATEGORIES,
)


class DannyHelp:
    """Inspired from R.danny's help menu"""

    async def format_bot_help(self, ctx: Context, help_settings: HelpSettings):
        description = ctx.bot.description or ""
        tagline = (help_settings.tagline) or self.get_default_tagline(ctx)
        if (
            not await ctx.embed_requested()
        ):  # Maybe redirect to non-embed minimal format
            await ctx.send("You need to enable embeds to use custom help menu")
        else:
            emb = {
                "embed": {"title": "", "description": ""},
                "footer": {"text": ""},
                "fields": [],
            }

            emb["footer"]["text"] = tagline
            if description:
                splitted = description.split("\n\n")
                name = splitted[0]
                value = "\n\n".join(splitted[1:])
                if not value:
                    value = EMPTY_STRING
                field = EmbedField(name[:252], value[:1024], False)
                emb["fields"].append(field)

            emb["title"] = f"{ctx.me.name} Help Menu"
            for cat in GLOBAL_CATEGORIES:
                cog_names = "`" + "` `".join(cat.cogs) + "`" if cat.cogs else ""
                for i, page in enumerate(
                    pagify(cog_names, page_length=1000, shorten_by=0)
                ):
                    if i == 0:
                        title = (
                            cat.reaction if cat.reaction else ""
                        ) + f"**{cat.name.capitalize()}:**"
                    else:
                        title = EMPTY_STRING
                    emb["fields"].append(EmbedField(title, cog_names, True))
            await self.make_and_send_embeds(
                ctx, emb, help_settings=help_settings, add_emojis=True
            )

    async def format_category_help(
        self, ctx: Context, obj: CategoryConvert, help_settings: HelpSettings
    ):
        coms = await self.get_category_help_mapping(
            ctx, obj, help_settings=help_settings
        )
        if not coms:
            return
        description = ctx.bot.description or ""
        tagline = (help_settings.tagline) or self.get_default_tagline(ctx)

        if await ctx.embed_requested():

            emb = {
                "embed": {"title": "", "description": ""},
                "footer": {"text": ""},
                "fields": [],
            }

            emb["footer"]["text"] = tagline
            if description:
                emb["embed"]["title"] = f"*{description[:250]}*"
            for cog_name, data in coms:
                if cog_name:
                    title = f"**{cog_name}**"
                else:
                    title = _("**No Category:**")

                cog_text = "\n" + " ".join(
                    (f"`{name}`") for name, command in sorted(data.items())
                )

                for page in pagify(cog_text, page_length=1000, shorten_by=0):
                    field = EmbedField(title, page, True)
                    emb["fields"].append(field)

            await self.make_and_send_embeds(ctx, emb, help_settings=help_settings)

        else:
            await ctx.send("Please have embeds enabled")