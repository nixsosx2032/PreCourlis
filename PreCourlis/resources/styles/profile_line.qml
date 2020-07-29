<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" readOnly="0" simplifyDrawingHints="1" simplifyMaxScale="1" version="3.10.3-A Coruña" labelsEnabled="0" simplifyDrawingTol="1" simplifyLocal="1" simplifyAlgorithm="0" maxScale="0" minScale="1e+8">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="0" type="line">
        <layer locked="0" class="SimpleLine" enabled="1" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,0,4,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" class="MarkerLine" enabled="1" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MM" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="vertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="@0@1" type="marker">
            <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory backgroundAlpha="255" sizeType="MM" barWidth="5" rotationOffset="270" width="15" penColor="#000000" scaleBasedVisibility="0" labelPlacementMethod="XHeight" minScaleDenominator="0" diagramOrientation="Up" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" penWidth="0" height="15" opacity="1" backgroundColor="#ffffff" scaleDependency="Area" minimumSize="0" maxScaleDenominator="1e+8" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" enabled="0">
      <fontProperties style="" description="Sans Serif,9,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" placement="2" obstacle="0" showAll="1" linePlacementFlags="18" dist="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="sec_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sec_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="abs_long">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="axis_x">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="axis_y">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="layers">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="p_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="abs_lat">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="zfond">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="sec_id" name=""/>
    <alias index="1" field="sec_name" name=""/>
    <alias index="2" field="abs_long" name=""/>
    <alias index="3" field="axis_x" name=""/>
    <alias index="4" field="axis_y" name=""/>
    <alias index="5" field="layers" name=""/>
    <alias index="6" field="p_id" name=""/>
    <alias index="7" field="abs_lat" name=""/>
    <alias index="8" field="zfond" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="sec_id"/>
    <default expression="" applyOnUpdate="0" field="sec_name"/>
    <default expression="" applyOnUpdate="0" field="abs_long"/>
    <default expression="" applyOnUpdate="0" field="axis_x"/>
    <default expression="" applyOnUpdate="0" field="axis_y"/>
    <default expression="" applyOnUpdate="0" field="layers"/>
    <default expression="" applyOnUpdate="0" field="p_id"/>
    <default expression="" applyOnUpdate="0" field="abs_lat"/>
    <default expression="" applyOnUpdate="0" field="zfond"/>
  </defaults>
  <constraints>
    <constraint constraints="0" field="sec_id" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="sec_name" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="abs_long" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="axis_x" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="axis_y" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="layers" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="p_id" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="abs_lat" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="zfond" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="sec_id" exp="" desc=""/>
    <constraint field="sec_name" exp="" desc=""/>
    <constraint field="abs_long" exp="" desc=""/>
    <constraint field="axis_x" exp="" desc=""/>
    <constraint field="axis_y" exp="" desc=""/>
    <constraint field="layers" exp="" desc=""/>
    <constraint field="p_id" exp="" desc=""/>
    <constraint field="abs_lat" exp="" desc=""/>
    <constraint field="zfond" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column hidden="0" width="-1" name="sec_id" type="field"/>
      <column hidden="0" width="-1" name="sec_name" type="field"/>
      <column hidden="0" width="-1" name="abs_long" type="field"/>
      <column hidden="0" width="-1" name="axis_x" type="field"/>
      <column hidden="0" width="-1" name="axis_y" type="field"/>
      <column hidden="0" width="-1" name="layers" type="field"/>
      <column hidden="0" width="-1" name="p_id" type="field"/>
      <column hidden="0" width="-1" name="abs_lat" type="field"/>
      <column hidden="0" width="-1" name="zfond" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="axis_x"/>
    <field editable="1" name="axis_y"/>
    <field editable="1" name="layers"/>
    <field editable="1" name="p_id"/>
    <field editable="1" name="abs_lat"/>
    <field editable="1" name="zfond"/>
    <field editable="1" name="sec_id"/>
    <field editable="1" name="sec_name"/>
    <field editable="1" name="abs_long"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="axis_x"/>
    <field labelOnTop="0" name="axis_y"/>
    <field labelOnTop="0" name="layers"/>
    <field labelOnTop="0" name="p_id"/>
    <field labelOnTop="0" name="abs_lat"/>
    <field labelOnTop="0" name="zfond"/>
    <field labelOnTop="0" name="sec_id"/>
    <field labelOnTop="0" name="sec_name"/>
    <field labelOnTop="0" name="abs_long"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>sec_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
