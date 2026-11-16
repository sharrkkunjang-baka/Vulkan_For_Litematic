# Vulkan_For_Litematic

装了 Aetherium 以后，Litematica 投影只剩蓝色轮廓，看不见砖块、玻璃等贴图？这个客户端补丁让方块模型正常显示。关光影能用，开光影也能用。蓝色差异提示照常保留。

## 先装什么

- **游戏：** Minecraft Java **26.3**、Java **25**、[Fabric Loader](https://fabricmc.net/use/installer/) **0.19.5+** 和 [Fabric API](https://modrinth.com/mod/fabric-api/versions?g=26.3) **0.161.0+**。视频设置里的图形 API 选 **Vulkan**，用的是游戏自带的 Vulkan，不需要装 VulkanMod。
- **光影核心：** [Aetherium 0.1.3（Fabric）](https://www.curseforge.com/minecraft/mc-mods/aetherium-vulkan-shader-mod/files/9545302) 和 [Sodium](https://modrinth.com/mod/sodium/versions?g=26.3) **0.9.2+**。这是给 **Aetherium** 用的补丁，不是 Iris 补丁；不要在这个实例里同时装 Iris 或 Vitrail。
- **投影：** [Litematica 0.29.1](https://modrinth.com/mod/litematica/version/0.29.1) 和它的前置 [MaLiLib 0.30.2](https://modrinth.com/mod/malilib/version/0.30.2)。

下好 [`Vulkan_For_Litematic.jar`](https://github.com/sharrkkunjang-baka/Vulkan_For_Litematic/releases/latest/download/Vulkan_For_Litematic.jar)，放进**客户端**的 `mods`，然后重开游戏。服务器不需要装。之前装过 `nyana-aetherium-schematic` 测试版的话，先移除旧 JAR，别同时保留两份。

## 光影包选哪个

| 光影包 | 支持情况 |
| --- | --- |
| 不开光影 | 已实测 |
| [BSL](https://modrinth.com/shader/bsl-shaders) **v10.1.8** | 已实测 |
| [Photon](https://modrinth.com/shader/photon-shader) **v1.4** | 已实测，包括同一局用 `K` 关掉再开 |
| [SEUS PTGI / PTGI HRR](https://www.sonicether.com/seus/) | **不支持**，不在本补丁的兼容范围内 |

光影包不是前置，本项目也不附带光影包。想开光影，把它的 ZIP 放进 `shaderpacks`，再在 Aetherium 里选择。其他光影包没有逐一测试；这个补丁不会让 Aetherium 原本加载不了的光影包变得可用。

![Photon v1.4 下的投影：玻璃、金块、砖块和石头的贴图正常显示](docs/photon.png)

<details>
<summary>原理和构建</summary>

Aetherium 扩展了地形顶点格式，Litematica 借这个格式写投影，却仍用自己的方块管线读取。补丁只让投影使用它自身管线的格式，不改游戏地形、差异层或光影合成。

用 Python 3 和 JDK 25，从已安装的 26.3 Fabric 客户端取编译依赖：

```sh
python build.py --minecraft-jar /path/to/minecraft-26.3.jar \
  --litematica-jar /path/to/litematica-fabric-26.3-0.29.1.jar \
  --libraries /path/to/.minecraft/libraries
```

输出为 `build/Vulkan_For_Litematic.jar`。代码采用 MIT 许可证；璃酱图标不包含在代码许可证内。

</details>
