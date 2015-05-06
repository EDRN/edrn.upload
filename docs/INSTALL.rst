edrn.rdf Installation
=====================

Use zc.buildout and the plone.recipe.zope2instance recipe to manage your project
and add ``edrn.rdf`` to your instance's eggs, or make ``edrn.rdf`` a dependency
of another egg that's included in your instance.
    
You don't need a ZCML slug with ``edrn.rdf`` since it uses
z3c.autoinclude.plugin with the Plone target.
