![ ](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Header.webp)
<a href="https://modrinth.com/mod/chime" target="_blank">
![req](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Requirements.webp)
</a>

  <p><strong>This Minecraft pack enhances the gameplay experience with the ViaBackwards plugin</strong>, which allow players to connect to newer servers with an older client. The pack requires the Chime mod to work, which helps identify the items by their custom name or custom NBT data, and assigns the correct model and texture to them. The best part of this pack is that if you put an another resourcespack on top of it, it will load the textures from that!<br><strong><span style="color: red;">Please note that this pack is not an official addon from the <a href="https://github.com/ViaVersion/ViaBackwards/graphs/contributors" target="_blank">ViaBackwards team</a>, and it's just fan-made.</span></strong></p>

![showcase_1.20](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Showcase%20.webp)

---

  ![Features](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_Features.webp)
  ![keypoints](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_KeyPoints.webp)

---

<a href="https://github.com/ViaVersionAddons/ViaBackwards-Plus/issues" target="_blank">
  
![reportissues](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_ReportIssues.webp)

</a>

---

<a href="https://bisecthosting.com/bangetto" target="_blank">
  
![sponsor](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_PromoCard.webp)

</a>

<hr>

<h3>Future plans <small>(<a href="https://ko-fi.com/bangetto" blank="_blank">Buy me a coffee</a> to make it happen sooner)</small></h3>
<ul>
  <li>Keep the pack up-today</li>
  <li><a href="https://github.com/ViaVersionAddons/ViaBackwards-Plus/issues/3" target="_blank">Port the pack to Optifine</a></li>
  <li>Create a custom ViaBackwards version for the smoothest experience</li>
  <li> Fix every bug</li>
  <li>Go below 1.16 (only if the pack get popular enought so I can ask the mod's dev to backport the mod)</li>
  <li>Add more easter eggs, maybe</li>
</ul>

---



![FAQ](https://www.bisecthosting.com/images/CF/ViaBackwards_Plus/BH_VBP_FAQ.webp)

<details>
<summary><b>Dependencies</b></summary>

**Chime**: The main priority of this project, the structure of the project is build upon Chime. It helps backporting the items in a fast and efficient way.

Optifine CIT: This is a work in progress more detailed in the next section, but it does the same thing, just  the implementation of it is a bit slower.

Respackopts: Used to fix the Minecraft logo in the main menu for 1.20-1.20.1, after it it done trough the overlay_pack feature. It is planned to use the capabilities of the mod more.


</details>

 <details>
<summary><b>Optifine?</b></summary>

**The Optifine versions of the pack is in the works, and will be done in the pack's 2.0 version with the release of Minecraft 1.21.**

The pack will start with the newly added and 1.17 items then it will move on to the 1.20 items and lastly do the 1.19 items, because there's a smaller Optifine pack called <a href="https://www.planetminecraft.com/texture-pack/viavisual/" target="_blank">ViaVisual</a>. If you want to speed up the development you can do it on <a href="https://github.com/ViaVersionAddons/ViaBackwards-Plus/tree/dev" target="_blank">Github</a>

</details>

<details>
<summary><b>Release Cycle</b></summary>

**As of Minecraft 1.20.5:**
When a Minecraft release is at Pre-release or Release-candidate stage a beta is released, but it's untested, so there's might be bugs. After a few days of the Minecraft release Viabackwards will also release publicly, this is when i'll fix bugs happened while the backporting, and after that the release of VB+ will be published.

</details>

<details>
<summary>How it Works?</summary>

<p>The pack works by identifying items by their ViaBackwards Protocol ID, which helps determine the correct model and texture to assign to them. For example, "Copper ore" has a protocol id of "44", the Chime mod will help the pack recognize it as a Copper ore and assign the correct model and texture to it.</p>
<p>Think of it like a special tag on each item that tells the pack what it is, so the pack knows how to make it look and behave correctly. This way, you get to enjoy the latest Minecraft textures and the easy identification of items, even if you're playing an older version of the game!</p>

</details>

<details>
<summary>Implementation on Servers</summary>

You can put this resources pack to your server so, it's automatically loads when players join. The only problem is that players still have to install Chime or CIT. As of now the resource pack has a more client-sided approach, but **a more server-side friendly version is planned!** If I see demand for it I will make and maintain a version of this pack which uses the vanilla `custom_model_data` feature to backport the items instead of the external ones. Join my Discord if you want to be notified when this happens!

</details>

<details>
<summary>Even lower versions?</summary>

#### If there's demand for it I can make support for 1.14x and 1.15x.

**For versions below that I probably won't, before 1.14 items had different ID's, which means the entire pack would have to be rewritten!** The only way to make the pack work for versions older then 1.14 would be Optifine CIT, and I hate to work with CIT, even `custom_model_data` was implemented in 1.14, Optifine had a monopoly back then...

</details>
