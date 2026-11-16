package nyana.schematic.mixin;

import com.mojang.renderpearl.api.vertex.VertexFormat;
import fi.dy.masa.litematica.render.schematic.BufferBuilderCache;
import fi.dy.masa.litematica.render.schematic.ChunkRenderLayers;
import net.minecraft.client.renderer.chunk.ChunkSectionLayer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(value = BufferBuilderCache.class, remap = false)
abstract class SchematicMeshFormatMixin {
    // Aetherium widens vanilla terrain's vertex binding for shader attributes, even with no pack active.
    // A schematic must instead write the format its own legacy terrain pipeline will read.
    @Redirect(method = "lambda$getBuilder$0",
        at = @At(value = "INVOKE", target = "Lnet/minecraft/client/renderer/chunk/ChunkSectionLayer;vertexFormat()Lcom/mojang/renderpearl/api/vertex/VertexFormat;"))
    private static VertexFormat useSchematicFormat(ChunkSectionLayer layer) {
        return ChunkRenderLayers.PIPELINE_MAP.get(layer).getLeft().getVertexFormatBinding(0);
    }
}
