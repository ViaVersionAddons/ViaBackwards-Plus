![ViaBackwards Plus logo](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Header.webp)

**This Minecraft pack enhances the gameplay experience with the ViaBackwards plugin**, which allows players to connect to newer servers with an older client. Rebuilt from the ground up for modern Minecraft, this pack requires **absolutely no mods** to work! It uses native vanilla features to identify future items by their component data and assigns the correct model and texture to them (officially supporting **1.21.4 through 1.21.11+**). The best part of this pack is that if you put another resource pack on top of it, it will load the textures from that (make sure to place this pack at the bottom)!

> **1.21.4 support:** Only works with ViaBackwards and ViaVersion version 5.9.0 or newer.
>
> **DISCLAIMER:** This pack is a fan-made project and is not an official addon from the [ViaBackwards team](https://github.com/ViaVersion/ViaBackwards/graphs/contributors).
>
> **SCOPE:** This pack specifically updates 2D inventory icons and in-hand 3D models. It does *not* change the textures of blocks or entities once they are physically placed in the world.

![Showcase of some item inventories when the pack is off versus on.](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Showcase%20.webp)

---

![Features](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Features.webp)
![Key points: Backports item textures from newer Minecraft versions. Compatible with other resource packs. Support down to 1.21.4, and all the way down to 1.16 with v1. Works even when the items are renamed!](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_KeyPoints.webp)

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
  <li>Try to integrate optifine or ETF textures for entities</li>
  <li>Fix every bug reported by the community</li>
  <li>Add more easter eggs, maybe</li>
</ul>

---

![FAQ](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_FAQ.webp)

<details>
<summary><b>Dependencies & Mods</b></summary>

**None!** The modern version of this project relies entirely on Minecraft's native `pack.mcmeta` overlays, `minecraft:component` rules, and the `custom_model_data` system. Players do not need Optifine, CIT, or Chime to see the new items. Just load the pack and play.

</details>

<details>
<summary><b>What about older versions?</b></summary>

This native vanilla approach is only possible because of engine changes introduced recently. **If you are looking to support clients older than 1.21.4**, you will need to use **Version 1** of this pack. 

Version 1 uses the Chime mod and Optifine CIT to backport items. You can still find Version 1 and its documentation in the <a href="https://github.com/ViaVersionAddons/ViaBackwards-Plus/tree/v1" target="_blank">v1 branch of this repository</a>.

</details>

<details>
<summary><b>Release cycle</b></summary>

**As of Minecraft 26.1:**
Our Base Pack will always target the newest Minecraft drops to ensure maximum compatibility for modern clients. When a new Minecraft version drops, ViaBackwards follows soon, and we'll update the base pack and push the previous version's items down into backward-compatible overlays. Expect updates shortly after major ViaBackwards protocol updates are published!

</details>

<details>
<summary><b>How it works</b></summary>

<p>Instead of relying on external mod IDs, this pack uses Minecraft's modern data-driven rendering engine. The pack is split into "overlays" to optimize loading for your particular version. </p>
<p>For example, when you join a 1.21.11 server using a 1.21.5 client, the server translates a new item (like a Copper Spear) into an item your client understands (like an Iron Sword) and attaches hidden component data to it. Our pack intercepts that specific data and says: <em>"Hey, this isn't actually an iron sword, render the Copper Spear model instead!"</em></p>

</details>

<details>
<summary><b>Implementation on servers</b></summary>

**This is the ultimate ViaBackwards server-side resource pack.** Because it no longer requires players to download third-party mods like Chime or Optifine, you can safely integrate this resource pack directly in your `server.properties`. When legacy players join your modern server, they'll automatically download the pack and immediately see the correct future items in their GUI!

</details>