#ifndef RICHARDSAPP_H
#define RICHARDSAPP_H

#include "MooseApp.h"

class RichardsApp;

template<>
InputParameters validParams<RichardsApp>();

/**
 * The Richards equation is a nonlinear diffusion
 * equation that models multiphase flow through
 * porous materials
 */
class RichardsApp : public MooseApp
{
public:
  RichardsApp(const std::string & name, InputParameters parameters);
  virtual ~RichardsApp();

  static void registerApps();
  static void registerObjects(Factory & factory);
  static void associateSyntax(Syntax & syntax, ActionFactory & action_factory);
};

#endif /* RICHARDSAPP_H */
