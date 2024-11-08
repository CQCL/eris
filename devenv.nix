{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [ pkgs.just ];

  languages.python = {
    enable = true;
    uv.enable = true;
  };
}
