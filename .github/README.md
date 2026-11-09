![ViaBackwards Plus logo](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Header.webp)

**This Minecraft pack enhances the gameplay experience with the ViaBackwards plugin**, which allows players on legacy clients (**1.16.4 through 1.20.4**) to connect to modern servers (up to **Minecraft 26.3**) and see all the new blocks, items, and weapons backported to their inventory! This legacy version (Version 1) uses **Chime** and **OptiFine CIT** to support older clients where modern vanilla component overrides do not exist. The best part of this pack is that if you put another resource pack on top of it, it will load the textures from that (make sure to place this pack at the bottom)!

> **Supported Clients:** Minecraft **1.16.4 through 1.20.4** *(Officially supported via Chime and OptiFine CIT. Minecraft 1.16.2 and 1.16.3 are also supported when using OptiFine).*

> **Supported Servers:** Connect to servers running anything from **1.17 all the way up through Minecraft 26.3** via ViaBackwards.

> **SCOPE:** This pack specifically updates 2D inventory icons and in-hand 3D models. It does *not* change the textures of blocks or entities once they are physically placed in the world.

![showcase_1.20](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Showcase%20.webp)

---

![Features](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Features.webp)
![keypoints](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_KeyPoints.webp)

---

<a href="https://github.com/ViaVersionAddons/ViaBackwards-Plus/issues" target="_blank">
  
![Report issues on GitHub or Discord](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_ReportIssues.webp)

</a>

---

<a href="https://bisecthosting.com/bangetto" target="_blank">
  
![Sponsored by BisectHosting. Rent a server: Use code BANGETTO for 25% off](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_PromoCard.webp)

</a>

<hr>

<h3>Future plans <small>(<a href="https://ko-fi.com/bangetto" blank="_blank">Buy me a coffee</a> to make it happen sooner)</small></h3>
<ul>
  <li>Keep the pack up-to-date with the newest Game Drops (26.x and beyond)</li>
  <li>Maintain parity with modern ViaBackwards protocol mappings</li>
  <li>Fix every bug reported by the community</li>
</ul>

---

![FAQ](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_FAQ.webp)

<details>
<summary><b>Dependencies & Recommended Setup</b></summary>

Because legacy Minecraft clients (1.16 – 1.20) lack modern vanilla model override capabilities, you need **one** of the following to see the backported models:

* **Fabric / Quilt (Recommended):** Use the **[Chime mod](https://modrinth.com/mod/chime)**. This provides the best overall performance and is 100% compatible with optimization mods like **Sodium, Iris, and Lithium**.
* **Fabric (1.17+):** You can alternatively use **[CIT Resewn](https://modrinth.com/mod/cit-resewn)**, which reads the pack's built-in OptiFine CIT files.
* **Forge / Standalone:** Fully supported using **OptiFine**. The pack includes complete CIT properties in `assets/minecraft/optifine/cit/`.

</details>

<details>
<summary><b>Playing on Minecraft 1.21.4 or newer?</b></summary>

**You do not want this version!** 

For clients running Minecraft **1.21.4+**, please use the modern **[Version 2 of ViaBackwards-Plus](https://github.com/ViaVersionAddons/ViaBackwards-Plus)**. Modern Version 2 requires **absolutely no mods** (no Chime, no OptiFine) and uses Minecraft's native data-driven model system.

</details>

<details>
<summary><b>Can I play on Minecraft 1.16.2 or 1.16.3?</b></summary>

**Yes, with OptiFine!**

CurseForge and Modrinth list **1.16.4 – 1.20.4** as the official range because the **Chime** mod requires Minecraft 1.16.4 or newer to install. 

However, internal item IDs and OptiFine CIT definitions are identical on 1.16.2 and 1.16.3. If you play on 1.16.2 or 1.16.3 with OptiFine, simply download the `.zip` manually from the "Files" tab and place it into your `resourcepacks/` folder.

</details>

<details>
<summary><b>What about Minecraft 1.20.5 through 1.21.3?</b></summary>

In Minecraft 1.20.5, Mojang overhauled items to use Data Components instead of NBT, which broke the Chime mod (Chime officially ended on 1.20.4). 

Clients running 1.20.5 through 1.21.3 can still load the backported item models using **OptiFine CIT**. However, if you are able to update to **1.21.4+**, we strongly recommend switching to modern **Version 2**, which requires zero mods.

</details>

<details>
<summary><b>Known Issues</b></summary>

**Tinted Items**: Vanilla Minecraft forces hardcoded biome and spawn-egg tints onto certain base items (like the Slime Spawn Egg or Short Grass). Because this pack maps newer items to these older carriers using `builtin/generated`, new custom foliage and spawn eggs may appear tinted or discolored in the player's inventory. This is an unavoidable vanilla rendering limitation on legacy clients.

</details>

<details>
<summary><b>How does it work?</b></summary>

<p>When you join a modern server (up to <strong>Minecraft 26.3</strong>) using an older client like 1.20.1 or 1.16.5, ViaBackwards translates future items into legacy items your client understands (such as turning a Mace into an Iron Sword) and attaches protocol identifiers to them.</p>

<p>This resource pack intercepts those identifiers and uses <strong>Chime</strong> or <strong>OptiFine CIT</strong> to override the model and texture, rendering the real future item right in your inventory and hand!</p>

</details>

<details>
<summary><b>Implementation on Servers</b></summary>

You can place this resource pack in your server's `server.properties` so legacy clients automatically prompt to download it upon joining. Note that legacy players still need **Chime** or **OptiFine** installed in their client mods to render the models. (If you want a 100% modless server experience, players must connect using 1.21.4+ clients with modern Version 2).

</details>

<br><br>

<hr>

<br>

<p align="center">This pack is a fan-made project and is not an official addon from the <a href="https://github.com/ViaVersion/ViaBackwards/graphs/contributors">ViaBackwards team</a></p> 
<p align="center">Minecraft assets are the property of Mojang Studios. Assets for showcase renders are sourced from <a href="https://github.com/Owen1212055/mc-assets">mc-assets</a>.</p>
